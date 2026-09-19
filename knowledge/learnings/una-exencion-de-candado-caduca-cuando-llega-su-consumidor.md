---
title: una exención de candado escrita "para el consumidor que vendrá" caduca el día que llega
date: 2026-09-20
source: agh-iberica
tags: [candados, gate, deuda]
---
Un corte previo (4a) dejó 10 exports marcados `@export-solo-para-test` porque en ese momento solo los
importaba su test. El corte siguiente (4b) escribió el endpoint que los consume de verdad → el candado
`exports-fantasma` se puso **rojo por las exenciones**, no por el código nuevo: una exención obsoleta
es un rojo duro, igual que la falta de una necesaria.

Patrón: toda anotación de la forma «esto está exento PORQUE todavía no lo usa nadie» tiene fecha de
caducidad implícita, y quien la agota es la PR siguiente, no la que la escribió. Al partir trabajo en
cortes, la limpieza de las exenciones del corte anterior **es parte del alcance del corte que trae el
consumidor** — no un hallazgo sorpresa a mitad del gate.

Corolario: un candado bien hecho falla en las DOS direcciones (falta exención / sobra exención). Si
solo falla en una, las exenciones se acumulan como deuda invisible.
