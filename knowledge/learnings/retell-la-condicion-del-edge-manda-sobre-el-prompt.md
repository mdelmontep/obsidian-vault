---
title: la condición de un edge de retell manda sobre cualquier regla del prompt
date: 2026-08-27
source: centro-elphis
tags: [retell, voz, conversation-flow, prompting]
---
Si la `transition_condition` de la única salida de un nodo exige un dato, **ninguna
instrucción del prompt consigue que el agente avance sin él**. No hay conflicto que
el LLM pueda resolver: sin dato no hay arista, y se queda dando vueltas en el nodo.

En Elphis el edge decía "el usuario tiene los 4 datos (relación, motivo, nombre,
consentimiento)". Quien no quería dar su nombre veía a Laura pedírselo cuatro veces
seguidas ignorando sus preguntas — el "bucle" que reportó la clienta. El prompt ya
decía "no insistas con el nombre"; daba igual.

Fix: el dato opcional sale de la condición y se convierte en política dentro de
ella ("el nombre NO es obligatorio para pasar: si ya lo has pedido dos veces, pasa
igualmente"). **Regla: en la condición va solo lo que de verdad bloquea el avance.**
