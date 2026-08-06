---
title: un campo numérico opcional que nadie escribe suma 0 y se lee como dato bueno
date: 2026-08-06
source: claude-code-session
tags: [typescript, tipos, coste, silencioso, facturaia]
---
Se añadió `coste_material_unit` a BD, a la RPC y a la UI. La columna existía, la
lectura la leía, la pantalla la pintaba. **Nadie la escribía**: los 6 INSERT del
snapshot mandaban `coste_mo_unit` y paraban ahí. Dos capas taparon el fallo:

1. El tipo del payload (`ObrasSnapshotLinea`) se quedó con las claves viejas, y
   los escritores usan `as ObrasSnapshotLinea` sobre literales parciales → el
   cast **silencia** el error.
2. El campo era opcional en el tipo de cálculo → omitirlo compila y suma 0.

Un `0` no parece un error: parece un coste. Salía "0,00 €" en la columna con la
que se decide qué ofertar a una subcontrata.

Fix estructural, no puntual: campos de coste **obligatorios** (el compilador te
lleva a los sitios) + test-candado que compara las claves del tipo con las que
devuelve la RPC, y falla en compilación Y en runtime si divergen. Pariente de
[[campo-opcional-en-tipo-compartido-no-implica-seleccionado-en-todos-los-selects]]
(aquel es la LECTURA, este la ESCRITURA).
