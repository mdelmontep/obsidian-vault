---
title: frontend — imágenes y assets
date: 2026-04-20
source: claude-md-migration
tags: [frontend, images, webp, assets]
---

# Frontend / Imágenes y assets

## Conversión de imágenes para web

- **`sips` no exporta a webp en macOS** — usar `cwebp -q 75-80 -resize 1600 0 input.png -o output.webp`. Reduce 2-5MB a 50-100KB consistentemente. No intentar `sips -s format webp`, da error "Can't write format".
- **Iconos de marcas reconocibles (WhatsApp, Instagram, Telegram, Messenger) deben usar SVG de marca real**, no iconos genéricos de Lucide. Lucide solo para conceptos genéricos (Email, Phone, Globe, Smartphone).
- **Overlays/fades sobre fotos: empezar ligeros** — opacidad máxima 0.45-0.55 en la zona oscura. Mejor poner poco y que el usuario pida más, que poner mucho y tener que reducir varias veces.

## Kommo page assets

- **Kommo K mark SVG** — el primer `<path>` de `public/images/kommo-logo.svg` es la K aislada (viewBox `0 0 26 28`). Reutilizable como componente `KommoK({ size, color })` en cualquier sección.
