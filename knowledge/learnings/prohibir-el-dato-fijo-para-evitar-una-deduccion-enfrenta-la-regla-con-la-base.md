---
title: prohibir el dato fijo para evitar una deducción enfrenta la regla con la base
date: 2026-09-13
source: centro-elphis
tags: [llm, prompt-engineering, retell, voz, elphis]
---
El fallo era deducir (Laura calculaba con la hora actual y decía "ahora está cerrado, mañana a las 9").
El fix prohibió también el dato que SÍ se sabe: *"Si preguntan por el horario: te lo confirma recepción"*,
con `Horario: L-V 9-21 h` intacto en la base de conocimiento. En llamada real dijo las dos cosas en dos
turnos seguidos: "te lo confirma recepción" y luego "de 9 a 21 horas". Una regla que contradice un dato
presente no lo oculta; lo convierte en una moneda al aire.

**Fix**: separar lo que el modelo no sabe (si está abierto AHORA) de lo fijo (el horario), prohibir solo
lo primero y dar lo segundo con frase literal. Medido en simulación: 0/3 → 3/3, y en transcript 6 → 0
envíos a recepción.

**Corolario de voz**: las cifras en formato 24 h se leen tal cual ("21 horas"). La forma de decirlas
("nueve de la noche") va en la misma línea que el dato → [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]].
