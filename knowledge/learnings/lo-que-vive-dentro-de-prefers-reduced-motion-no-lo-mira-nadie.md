---
title: lo que vive dentro de prefers-reduced-motion no lo mira nadie
date: 2026-08-03
source: claude-code-session
tags: [css, accesibilidad, ui, deuda]
---
Tres defectos del mismo barrido estaban **los tres** dentro de `@media (prefers-reduced-motion: reduce)`.
No es casualidad: ese ramal no lo ejecuta ningún test, no sale en ninguna captura y nadie hace QA con la
preferencia activada, así que el CSS de dentro envejece sin que nada lo toque.

Los tres, y ninguno da error:
- `translateX(var(--x))` con `--x` **sin declarar** → la declaración es inválida y el valor cae a 0. Al
  pulsar un interruptor ENCENDIDO el mando saltaba a la posición de apagado.
- `animation: none` sobre una barra de progreso → se **congela al 100%**. El temporizador vive en JS y
  sigue corriendo: promete tiempo que no queda. **Ocultarla es más honesto que congelarla.**
- Salto a relleno completo en un botón de mantener-pulsado → mata la única señal de cuándo dispara una
  acción irreversible.

Regla: `reduce` significa *quitar movimiento decorativo*, **no** *quitar información*. Un indicador de
progreso en curso no es decoración — ralentízalo o cámbialo por texto, nunca lo congeles ni lo saltes.
Al tocar un componente animado, abre su bloque `reduce` y léelo: es donde se acumula la deuda invisible.

Ver [[css-animation-transform-pisa-transform-estatico]] · [[token-de-relleno-no-sirve-como-token-de-texto]]
