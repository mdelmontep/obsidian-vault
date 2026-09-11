---
title: capturar pantalla con la url visible exige dos permisos distintos de macos
date: 2026-09-11
source: laserys-las-rozas
tags: [macos, screenshots, soporte, chrome]
---

Soporte (Kommo, Meta, cualquiera) pide capturas **sin recortar y con la URL visible**: hay que fotografiar la pantalla real, no usar el screenshot del navegador automatizado (recorta el viewport y no muestra la barra de direcciones).

Dos permisos **separados** en Ajustes → Privacidad y seguridad, y fallan distinto:
- **Grabación de pantalla** para `screencapture -x -o`. Sin él: `could not create image from display`.
- **Automatización** (Apple Events) para traer la pestaña correcta al frente con AppleScript. Sin él: `No tienes autorización para enviar eventos Apple a Google Chrome. (-1743)` — y **la captura sale igual, de la pestaña equivocada**: error silencioso de cara al resultado.

Atajo que evita el segundo permiso: `open -a "Google Chrome" "<url>"` (activa la app y la pestaña de esa URL), `sleep 2`, `screencapture -x -o f.png`.

Verificar cada captura antes de entregarla con una miniatura barata — `sips -Z 900 f.png --out /tmp/t.png` — y no un `Read` del PNG a tamaño completo.
