---
title: scroll-snap para filter chips: Material M3 lo desaconseja
date: 2026-05-18
source: claude-code-session
tags: [css, ux, material, scroll]
---

Material Design 3 chips guidelines: `scroll-snap-type` genera saltos al tener chips de anchos variables (texto variable). OK para carousels de tarjetas ancho fijo.

Gmail, YouTube, Twitter NO snappean chips de filtro. Apple HIG tampoco lo menciona para controles selección.

Affordance recomendada = fade hint Komarov, no snap. Ver [[scroll-shadows-komarov-con-css-variable-dark-mode]].

M3: https://m3.material.io/components/chips/guidelines
