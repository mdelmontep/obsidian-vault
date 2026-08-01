---
title: jsdom no reproduce el reset de selección al cambiar input.type
date: 2026-08-01
source: claude-code-session
tags: [testing, jsdom, react, inputs, facturaia]
---

Reasignar `input.type` en un navegador **resetea la selección a (0,0)**. jsdom no lo hace.
Un componente que alterna `number`↔`text` para controlar el formato y luego lee
`selectionStart` para saber dónde insertar, en el navegador inserta siempre al principio:
tecleas 1, 2, 3 y queda **321**. En jsdom pasa verde.

- Agravante: el test unitario llamaba a `setSelectionRange` a mano antes de cada tecla, o
  sea que además simulaba el escenario bueno. Doble ceguera.
- Para tener red: parchear el setter de `type` del nodo para que pierda la selección, y
  teclear **sin tocar la selección entre pulsaciones**. Con eso el bug sale en rojo.
- Regla: un componente que manipula `type`, `selectionStart` o el setter nativo de `value`
  no se puede dar por cubierto con jsdom. O test de navegador, o un doble que reproduzca
  ese efecto concreto.

Caso real: FacturaIA `number-field.tsx`, 67 ficheros consumidores, llegó a producción y lo
cazó un gate de cierre conduciendo el navegador, no la suite (PR #1446).
