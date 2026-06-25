---
title: migrar input nativo a componente wrapper — superar/borrar las reglas css del nativo
date: 2026-06-25
source: claude-code-session
tags: [css, design-system, frontend, facturaia]
---

Al sustituir un `<input>` nativo (checkbox/radio/number) por un componente que lo
envuelve y lo estiliza, las reglas CSS contextuales del sitio (`.padre input`,
`.wrapper input[type=x]`) suelen tener MÁS especificidad que las clases del
componente y lo pisan.

- **Checkbox/radio con overlay transparente** (`input{position:absolute;inset:0;
  width:100%;opacity:0}`): `.wrapper input[type=checkbox]{width:16px}` (0,2,1) gana a
  `.input{width:100%}` (0,1,0) → encoge el área clicable, bordes muertos. Fix: BORRAR
  las reglas del nativo al migrar (no tocar `input[type=radio]` ni el switch/Toggle).
- **Number con stepper**: `.edit-row input` (0,1,1) / `.admin-cobros-pricing-tr
  input[type=number]` (0,1,2) pisan `.inputStepper{padding-right}` (0,1,0) → el número
  queda bajo las flechas. Fix: selector COMPUESTO `.input.inputStepper` (0,2,0) gana a
  todo lo contextual.

Corolarios: wrapper `<span>` no `<label>` (anidable en un `<label>` externo, sin doble
toggle); en flex-row de ancho fijo el wrap colapsa → pasar `wrapClassName` con el ancho.

Caso real FacturaIA: checkbox "Burst" + NumberField, fuente única (docs/design §6-7).
