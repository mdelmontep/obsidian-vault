---
title: floating-ui strategy por defecto (absolute) con CSS position:fixed desplaza el elemento
date: 2026-07-06
source: claude-code-session
tags: [frontend, react, floating-ui, css, tooltip]
---

`useFloating()` de `@floating-ui/react` calcula `top`/`left`/`transform:translate()`
asumiendo `strategy: 'absolute'` (el valor por defecto) salvo que se indique lo
contrario. Si el CSS del elemento flotante fija `position: fixed` (habitual al
portar a `<body>` con `FloatingPortal`), el navegador aplica coordenadas
calculadas para "absolute" a un elemento "fixed" — el resultado visual: el
tooltip/popover aparece desplazado hacia la esquina superior izquierda (tanto
más cuanto más scroll haya en la página).

Fix: pasar `strategy: 'fixed'` explícito a `useFloating()` cuando el CSS use
`position: fixed` (recomendado al portar a `<body>`, evita problemas con
scroll containers). Deben coincidir siempre — es una pareja config+CSS, no un
valor que se pueda fijar en un solo sitio y olvidar el otro.

Caso: TuFacturaIA `src/components/ui/tooltip.tsx`. Ver [[floating-ui-usedelaygroup-auto-registra-currentid]] · [[react-hooks-refs-falso-positivo-floating-ui]].
