---
title: react-pdf font register usa rutas filesystem no urls
date: 2026-04-26
source: claude-code-session
tags: [react-pdf, nextjs, docker, fonts]
---

# `@react-pdf/renderer` Font.register interpreta rutas como filesystem, no URLs

`Font.register({ src: '/fonts/Filson-Soft-Regular.ttf' })` en Node.js server se interpreta como ruta absoluta de filesystem: busca `/fonts/Filson-Soft-Regular.ttf` desde la raíz del sistema.

**En Docker standalone** (node:20-alpine, WORKDIR /app): falla con `ENOENT: no such file or directory, open '/fonts/Filson-Soft-Regular.ttf'`.

**Fix**: usar `path.join(process.cwd(), 'public', 'fonts', 'Filson-Soft-Regular.ttf')` que resuelve a `/app/public/fonts/...` en el contenedor.

**Verificar en Dockerfile**: que `public/fonts/` se copie al stage runner (`COPY --from=builder /app/public ./public`).

**Nota**: en el browser (client-side), `/fonts/...` funciona como URL relativa al origen. El problema es exclusivamente server-side. Si el componente se usa en ambos contextos, usar la ruta absoluta con `path.join` — funciona en ambos porque en el browser `@react-pdf/renderer` usa su propio loader.
