---
title: menú/popover portal posicionado por rect.bottom se sale del viewport en filas bajas
date: 2026-06-17
source: claude-code-session
tags: [frontend, ui, react, portal, playwright]
---

Un menú/popover en portal (`document.body`) posicionado con `top = rect.bottom + 4`
(rect del botón) cae FUERA del viewport cuando la fila/botón está en la parte baja
de la pantalla → sus items quedan inalcanzables: están en el DOM y "visibles", pero
fuera de los límites del viewport (Playwright falla el click con "outside of the
viewport"; un usuario tampoco llega).

Fix (flip vertical): si `innerHeight - rect.bottom < altoEstimadoMenú` y hay más sitio
arriba (`rect.top > spaceBelow`), anclar el menú por su borde inferior sobre el botón
(`bottom = innerHeight - rect.top + 4`, abre hacia arriba) en vez de por `top`. El estado
del menú lleva `top?` o `bottom?` y el style usa el que esté.

Caso FacturaIA #355: "Eliminar" un borrador en /emitidas no abría el confirm — era esto.
Mismo patrón en /recibidas y /presupuestos. Reproducido y verificado con Playwright.

Actualización (2026-06-18, PR #376): el cálculo manual de flip (altura ESTIMADA) era
frágil → flip prematuro y menú descolgado del trigger. Migrado a `@floating-ui/react`
(`useAnchoredMenu`): `flip()` mide altura real y solo voltea si no cabe. Preferir Floating
UI sobre cálculo a mano. Ver [[react-hooks-refs-falso-positivo-floating-ui]] · ADR-033.
