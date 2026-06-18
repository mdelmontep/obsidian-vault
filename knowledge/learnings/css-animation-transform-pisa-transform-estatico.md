---
title: animación @keyframes con transform final pisa el transform estático del elemento
date: 2026-06-17
source: claude-code-session
tags: [frontend, css, animation, portal, posicionamiento]
---

Una animación `@keyframes` cuyo estado final fija `transform` SOBREESCRIBE cualquier
`transform` estático/inline del mismo elemento (el `to {}` gana mientras la animación
está aplicada, y se queda con `animation-fill-mode` o si el `to` = estado en reposo).

Síntoma real (FacturaIA, menú ⋯ de Equipo): el menú en portal se anclaba con
`left = rect.right` confiando en un `transform: translateX(-100%)` "del CSS" para
pegar su borde derecho al botón. Pero `.row-menu` animaba con `menuFadeIn` que termina
en `transform: translateY(0)` → el translateX nunca se aplicaba → el menú abría hacia
la derecha, fuera de pantalla.

Fix robusto: anclar portales posicionados con las PROPS CSS `right`/`left`
(`right = innerWidth - rect.right`), nunca vía `transform`, si el elemento además anima.
Patrón ya usado en clientes/facturas/presupuestos del mismo repo. Ver [[menu-portal-flip-viewport]].

Aplica también a `@floating-ui/react`: sus `floatingStyles` posicionan con `transform`
por defecto → mismo choque con animaciones de apertura. Configurar el hook para posicionar
con `top/left` (usar `x/y/strategy`, no `floatingStyles`). FacturaIA PR #376 (`useAnchoredMenu`).
