---
title: next/image rompe en puppeteer y renderizado server-side
date: 2026-04-28
source: claude-code-session
tags: [nextjs, pdf, puppeteer, templates]
---

`next/image` es un componente client-only. En contexto server-side (Puppeteer, `renderToString`, API routes) lanza `Cannot access Image.prototype on the server`.

**Síntoma**: `pdf_url: null` en la respuesta — el catch lo silencia y la factura se crea sin PDF.

**Fix**: usar `<img>` nativo en todas las plantillas que se rendericen server-side. Los atributos `width` y `height` van en `style` inline, no como props.

**Regla**: plantillas de PDF = HTML/CSS puro. Sin componentes Next.js, sin hooks, sin imports de `next/*`.
