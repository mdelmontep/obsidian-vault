---
title: sips no exporta webp en macos usar cwebp
date: 2026-04-16
source: claude-code-session
tags: [macos, imagenes, web, frontend]
---

`sips -s format webp` falla en macOS con error "Can't write format: org.webmproject.webp". No es un problema de permisos ni de versión — sips simplemente no soporta escritura webp.

Alternativa fiable: `cwebp` (de libwebp, instalable via Homebrew).

```bash
# Conversión estándar para assets web
cwebp -q 75-80 -resize 1600 0 input.png -o output.webp
```

- `-q 75-80`: calidad suficiente para web, buen equilibrio tamaño/calidad
- `-resize 1600 0`: ancho máximo 1600px, alto proporcional (0 = auto)
- Resultados típicos: 2-5MB PNG/JPG → 50-100KB webp
