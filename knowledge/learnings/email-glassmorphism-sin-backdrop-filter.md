---
title: glassmorphism en email sin backdrop-filter
date: 2026-06-23
source: claude-code-session
tags: [email, css, design]
---

`backdrop-filter:blur()` no funciona en ningún cliente de email.

**Simulación glass que sí funciona:**
- Fondo gradiente claro en el wrapper (`linear-gradient` en `bgcolor` de tabla outer)
- Card con `border:1px solid rgba(61,123,245,0.15)` + `box-shadow` capas (difuso + suave)
- Secciones internas con `background:rgba(61,123,245,0.05)` + borde rgba

**Animaciones CSS en email:**
- `@keyframes` funciona en Apple Mail (macOS/iOS) y algunos clientes modernos
- Outlook ignora CSS animations; recibe el estado estático
- Patrón: animar el elemento HTML (`<a>`, `<span class="btn-anim">`) con `<!--[if !mso]><!-- -->` guard
- Stripe superior: `background-size:300%` + `animation:stripe` → efecto de movimiento de gradiente

**VML para Outlook:** siempre envolver el CTA con `<!--[if mso]>...<![endif]-->` bulletproof.

**Webfont con carácter:** progressive enhancement — `@import` en `<style>` la cargan Apple Mail/iOS; Gmail/Outlook caen a la pila websafe (nunca crítica). La distinción real la dan color/composición, no la fuente.
