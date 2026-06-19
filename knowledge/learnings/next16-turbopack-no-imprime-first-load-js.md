---
title: next 16 + turbopack no imprime la tabla first load js en build
date: 2026-06-19
source: claude-code-session
tags: [next, performance, turbopack]
---
`next build` con Turbopack (Next 16) ya NO imprime la columna Size / First Load JS
por ruta (sí lo hacía con Webpack). Para medir el peso del bundle cliente:
- Total y top chunks: `du -k .next/static/chunks/*.js | sort -rn`.
- Qué librería es cada chunk gordo: `grep -ao "recharts\|pdfjs\|@supabase\|zod\|react-dom" <chunk>` (los nombres de paquete sobreviven minificados).
- First-load compartido (cada página): `.next/build-manifest.json` → `rootMainFiles` (suma el tamaño de esos ficheros).
No te fíes de un identificador minificado suelto (p.ej. "framer" ≠ framer-motion); confírmalo contra `package.json`.
Ver [[ssr-seed-contra-cls-de-client-fetch-en-app-router]] · [[medir-cwv-autenticado-sin-lighthouse]].
