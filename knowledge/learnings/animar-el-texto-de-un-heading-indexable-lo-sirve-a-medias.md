---
title: animar el texto de un heading indexable lo sirve a medias a crawlers y lectores de pantalla
date: 2026-08-01
source: claude-code-session
tags: [seo, a11y, frontend, animacion, landing]
---

Efecto máquina de escribir (o `TextRoll` letra a letra) escribiendo sobre el
`textContent` del propio `<h1>`/`<h2>`: quien muestrea el DOM en un instante
cualquiera —Googlebot, lector de pantalla, test— lo coge a mitad de tecleo.
Medido en agentesia-web: **un tercio de las muestras** daba `"no pe"` o
`"Agentes de IA pararespond"`; el H2 con TextRoll daba `"T T e e c c…"` por los
spans por letra.

Patrón correcto — **el heading nunca es el elemento animado**:

- El texto del heading es un nodo estable y completo, se prerenderiza y no se
  reescribe jamás.
- La rotación vive en una capa hermana `aria-hidden="true"` **fuera** del
  heading, con crossfade de frase completa (`AnimatePresence`), no tecleo.
- El hueco lo reserva un *sizer* con la frase más larga (`visibility:hidden`),
  así rotar no cambia la altura del bloque.
- Fuera el caret: ya no describe lo que hace la animación.

Candado: test que lea `h1.textContent` en ~20 muestras a lo largo del ciclo de
rotación y exija siempre la frase entera. Sin él la regresión vuelve invisible.

Corolario: `prefers-reduced-motion` **no** es el arreglo — solo tapa el fallo
para quien lo tiene activo. Ver [[agentesia]].
