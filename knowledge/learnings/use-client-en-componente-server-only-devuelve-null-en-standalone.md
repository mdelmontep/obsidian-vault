---
title: use client en componente server-only devuelve null en standalone
date: 2026-04-26
source: claude-code-session
tags: [nextjs, standalone, react-pdf, server-components]
---

# `'use client'` en componente solo importado server-side devuelve null en standalone

Cuando un componente tiene `'use client'` pero solo se importa desde API routes (server-side), Next.js standalone reemplaza el export real por un **client reference placeholder** (null).

**Síntoma**: `TypeError: Cannot read properties of null (reading 'props')` al pasar el componente a `renderToBuffer()` o `createElement()`.

**Caso real**: `InvoicePDF` en FacturaIA tenía `'use client'` porque originalmente se usaba en preview del browser. Al moverlo a solo server-side (API route `/api/voice/generate`), el standalone lo anulaba.

**Fix**: quitar `'use client'` si no hay consumidores client-side. Si hay consumidores de ambos lados, extraer la lógica pura a un archivo sin directiva e importar desde ambos.

**Cómo detectarlo**: si un componente React devuelve `null` en producción pero funciona en dev, revisar si tiene `'use client'` y se importa desde un Route Handler o API route.

Ver también [[puppeteer-html-to-pdf-pixel-perfect-con-plantillas-react]] (punto 3)
