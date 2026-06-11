---
title: contraste APCA como gate reproducible en script node sobre tokens css
date: 2026-06-11
source: claude-code-session
tags: [css, accesibilidad, design-system]
---
WCAG 2 ratio falla en dark mode (sobrestima contraste de claros sobre oscuro). APCA
(SAPC/APCA-W3 0.0.98G-4.2, ~60 líneas) se implementa inline en un script Node
(`scripts/apca-audit.mjs` en TuFacturaIA) que valida pares token/fondo y sale !=0 si falla.
Umbrales por uso, no globales: Lc 90 cuerpo · Lc 60 texto secundario corto no-cuerpo ·
Lc 30 placeholders/disabled · Lc 15 bordes.
Gotcha: Lc 75 para `--muted` en dark es inalcanzable sin acercarlo a `--fg-soft` (mata la
jerarquía visual) → bajar el requisito a 60 y documentar por qué, no forzar el color.
Patrón clave: texto semántico SIEMPRE via tokens `*-fg` dedicados; los base
(`--brand/--ok/--warn/--danger`) quedan para rellenos/botones/iconos donde el contraste
lo da el contexto, no el texto.
