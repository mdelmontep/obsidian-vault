---
title: contenido de un LLM en un PDF → renderizar como nodos React, nunca HTML crudo
date: 2026-06-19
source: claude-code-session
tags: [pdf, seguridad, llm, react, puppeteer, facturaia]
---

Para meter contenido NO confiable de un LLM (p.ej. texto que el agente MCP aporta a un presupuesto) en un PDF renderizado con React SSR + Puppeteer:

- Renderízalo como **nodos React** construidos a partir del texto parseado → React **escapa** todo por defecto. NUNCA `dangerouslySetInnerHTML` ni HTML crudo del LLM.
- Para "markdown acotado": parser propio mínimo (negrita/cursiva/listas/saltos) → `<strong>/<em>/<ul>/<p>`. Evita markdown→HTML→DOMPurify: DOMPurify necesita un DOM (jsdom) server-side y añade superficie; el parser-a-React es más simple y seguro.
- Backstop del PDF: `setJavaScriptEnabled(false)` + `setRequestInterception` (solo `data:`+imágenes https) + CSP `default-src 'none'`. Así, aunque algo se colara, no ejecuta.
- Test obligatorio: que `<script>`/`<img onerror>` del input salgan ESCAPADOS (`&lt;script&gt;`), no como tags.

Caso: W3 conector MCP, `markdown-mini.tsx` + 4 templates de presupuesto. Ver [[puppeteer-html-to-pdf-pixel-perfect-con-plantillas-react]].
