---
title: puppeteer html-to-pdf pixel-perfect con plantillas react
date: 2026-04-25
source: facturaia — sesión plantillas documentos
tags: [puppeteer, pdf, react, nextjs, facturaia]
---

# Puppeteer HTML→PDF pixel-perfect con plantillas React

Patrón para generar PDFs que sean idénticos al preview HTML del navegador, usando Puppeteer headless Chrome + `renderToStaticMarkup`.

## Problema

`@react-pdf/renderer` usa su propio layout engine (yoga) que no soporta CSS grid, gap, mask-image, etc. El resultado nunca coincide con el preview HTML. `pdf-lib` es aún más limitado (solo texto y rectángulos).

## Solución: Puppeteer + renderToStaticMarkup

```
React component → renderToStaticMarkup() → HTML string → page.setContent() → page.pdf() → Buffer
```

### Arquitectura

1. **API Route** (`/api/render-pdf`): recibe `{ config, data }`, importa dinámicamente el componente de plantilla y `react-dom/server`
2. **Browser singleton**: instancia de Puppeteer reutilizada con idle timeout de 60s
3. **Fonts embebidas**: woff2 → base64 inline en `<style>` (evita network round-trip)
4. **Font cache**: `Map<filename, base64_face>` a nivel de módulo (no re-lee de disco)
5. **Per-template fonts**: cada plantilla carga solo sus 2-3 fuentes, no las 10 del catálogo

### Gotchas Next.js 16

- **`renderToStaticMarkup` bloqueado como import estático** en Route Handlers. Error: "You're importing a component that imports react-dom/server". Fix: `await import('react-dom/server')` dinámico
- **`'use client'` en componentes de plantilla** impide llamarlos desde server. Fix: quitar la directiva si son funciones puras sin hooks. Siguen funcionando client-side porque el padre tiene `'use client'`
- **Middleware intercepta API routes** — excluir `/api/render-pdf` en `isServiceRoute`

### Performance

| Optimización | Impacto |
|---|---|
| Browser singleton (no launch por request) | ~8s → ~3s |
| `page.setContent()` vs `page.goto()` | Elimina round-trip al dev server |
| Per-template fonts (2-3 vs 10) | ~500ms menos |
| Font base64 cache en memoria | ~200ms menos en requests siguientes |
| `waitUntil: 'load'` vs `networkidle0` | ~500ms menos |

Resultado: cold start ~10s, warm ~2.3s.

### Código clave

```typescript
// Dynamic imports (obligatorio en Next.js 16 Route Handlers)
const { renderToStaticMarkup } = await import('react-dom/server')
const { createElement } = await import('react')
const mod = await import(`@/components/templates/template-${tid}`)
const Component = mod[Object.keys(mod)[0]]

// Render HTML con fonts embebidas
const templateHtml = renderToStaticMarkup(createElement(Component, { config, data }))
const html = `<!DOCTYPE html><html><head><style>${fontFaces.join('')}...</style></head><body>${templateHtml}</body></html>`

// PDF
await page.setContent(html, { waitUntil: 'load' })
const pdfBuffer = await page.pdf({ format: 'A4', printBackground: true, margin: { top: '0', ... } })
```

## Cuándo usar

- Cuando el preview HTML usa CSS avanzado (grid, gradients, mask-image, backdrop-filter)
- Cuando se necesita pixel-perfect entre preview y PDF
- Cuando hay múltiples plantillas con diseños muy diferentes

## Cuándo NO usar

- PDFs simples tipo recibo → `pdf-lib` es suficiente y más ligero
- Entornos serverless sin soporte para Chrome (Vercel Edge) → usar `@react-pdf/renderer` o servicio externo
