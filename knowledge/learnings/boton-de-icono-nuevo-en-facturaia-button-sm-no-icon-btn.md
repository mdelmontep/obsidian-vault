---
title: botón de icono nuevo en facturaia — <Button size="sm">, no .icon-btn nativo
date: 2026-08-12
source: claude-code-session
tags: [facturaia, frontend, design-system, gates]
---

Dos guardas del repo parecen apuntar a soluciones opuestas y solo una vale
para código NUEVO. El censo tap-target (`tap-target-inventario.test.ts`) tiene
vecinos viejos con `.icon-btn.sm` nativo y notas que lo elogian → imitar eso
en un fichero nuevo dispara el OTRO guard: el trinquete de deuda de diseño
(`design-debt-ratchet.mjs`, pre-commit) bloquea todo `<button>` nativo fuera
del baseline.

Respuesta correcta en ficheros nuevos: `<Button variant="ghost" size="sm">`
del primitivo (acepta `className` y atributos nativos para headers colapsables
y filas clicables) + registrar la entrada en
`docs/architecture/tap-target-inventario.json` con su `disposicion` — el
primitivo ya sube el objetivo táctil a 44px bajo `pointer:coarse`, así que
`sm` es correcto en listas cortas tipo settings (xs solo en filas densas).
