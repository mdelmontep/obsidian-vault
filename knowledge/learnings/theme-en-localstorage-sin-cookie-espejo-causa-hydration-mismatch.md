---
title: preferencia de tema solo en localStorage (sin cookie espejo) causa hydration mismatch en cada carga
date: 2026-07-15
source: claude-code-session
tags: [react, ssr, hydration, nextjs, theming]
---

Si el tema claro/oscuro se guarda SOLO en `localStorage` (ej. TuFacturaIA
`use-theme.ts`, clave `af-theme`) y el servidor no tiene forma de leerlo, el SSR
siempre renderiza un tema por defecto (light) y el cliente lo corrige tras
hidratar. Resultado: cualquier usuario con tema oscuro guardado dispara un
`Hydration mismatch` de React en CADA carga de página (visible en consola:
"A tree hydrated but some attributes... didn't match"), típicamente en el botón
de toggle (`aria-label` distinto servidor/cliente). No rompe visualmente (React
lo corrige), pero es ruido de consola permanente y indica que el patrón correcto
—resolver el valor inicial en servidor, como ya hace el `isMobile` de la misma
app vía User-Agent— no se aplicó al tema.

Fix general: mirror del valor en una cookie (`Set-Cookie` al cambiar el toggle) y
leerla en el layout server component para fijar el `data-theme`/`initial` correcto
antes del primer render, en vez de depender solo de `localStorage` + corrección
post-mount. Encontrado en TuFacturaIA (2026-07-15), no corregido — preexistente,
fuera de alcance de la sesión que lo detectó. Ver [[facturaia]].
