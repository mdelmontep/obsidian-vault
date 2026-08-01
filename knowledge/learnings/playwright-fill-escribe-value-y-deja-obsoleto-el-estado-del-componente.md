---
title: playwright fill escribe .value y deja obsoleto el estado interno del componente
date: 2026-08-01
source: claude-code-session
tags: [e2e, playwright, react, inputs, facturaia]
---

`fill()` **no selecciona ni teclea**: escribe `.value` directo y dispara `input`. Un
componente controlado que lleva su propio texto lógico en un ref y lo compara con el DOM ve
que divergen y cae en su rama de "append", así que `fill('30')` sobre un campo que vale `7`
deja **730**. `fill('')` antes tampoco basta: el ref sigue con el valor viejo.

- Distinguir siempre **bug del componente** de **artefacto de la automatización** antes de
  abrir un ticket: aquí el tecleo humano real daba bien y el `fill` mal.
- Recetas que sí funcionan sobre un input así: `fill('')` + `blur()` + `fill(valor)`, o
  `focus()` + seleccionar todo + teclas reales, o backspaces hasta vaciar.
- `Meta+A` **no llega al campo** por automatización: quien mida con esa tecla creerá que
  hay un bug donde no lo hay.
- Queda un hueco real derivado: si la propia app reescribe el valor mientras el campo está
  enfocado, sigue el mismo camino que el `fill`.

Ver [[jsdom-no-reproduce-el-reset-de-seleccion-al-cambiar-input-type]].
