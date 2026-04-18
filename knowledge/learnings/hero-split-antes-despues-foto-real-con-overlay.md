---
title: hero split "antes/después" con foto real necesita overlay blanco + shadow fuerte
date: 2026-04-16
source: claude-code-session
tags: [frontend, motion, layout, design, kommo]
---

Patrón: card izquierda = ventanas caóticas apiladas (el "antes"), card derecha = foto real de fondo + mock panel flotante (el "después"). La foto compite con el mock si se deja limpia.

Reglas obligatorias para que funcione:

1. **Gradiente blanco vertical encima de la foto**: `linear-gradient(180deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.55) 55%, rgba(255,255,255,0.85) 100%)`. Sin esto, el mock flotante no tiene contraste en la mitad superior.

2. **Mock con shadow fuerte + borde sutil**: `boxShadow: "0 16px 44px rgba(0,0,0,0.14), 0 2px 12px rgba(130,113,255,0.12)"` + `border` a color neutro. Sin shadow el mock parece pegado en Paint.

3. **Mock anclado al borde inferior**: `absolute bottom-5 left-5 right-5`. Centrarlo verticalmente rompe la jerarquía — debe sentirse que flota sobre la escena real.

Entrada con bounce suave: `ease: [0.34, 1.3, 0.64, 1]`, `delay: ~0.95`, `initial={{ opacity: 0, y: 20, scale: 0.95 }}`.

Ejemplo: `src/components/sections/kommo-page/HeroSwarm.tsx` en `new-project-setup` — "Antes" = 6 ventanas rotadas con badges rojos de no leídos, "Después" = foto real del dueño del negocio + panel Kommo con 3 conversaciones.
