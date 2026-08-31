---
title: antes de inventar un protocolo, mirar si el esquema ya lo codifica
date: 2026-08-31
source: facturaia
tags: [prompting, documentacion, qa]
---
Escribí en un prompt de continuación un método de dos pases —defender una afirmación, luego
atacarla— con su justificación y sus reglas. Al revisarlo encontré que el barrido ya lo tenía
**en el esquema de datos**: `docs/qa/refutacion/v2/*.jsonl` lleva `veredicto_carril` +
`severidad_carril` (la defensa) y `veredicto_refutador` + `severidad_final` + `razon` (el
ataque), con 63 líneas ya escritas.

El prompt no estaba mal, estaba **huérfano**: pedía «los dos pases escritos» sin decir dónde,
así que la siguiente sesión se habría inventado un formato y habría fragmentado el registro.

Regla: cuando vayas a escribir un proceso, `ls` y `head -c 400` de los ficheros de datos del
área antes que la primera frase. Un campo de un JSONL ya existente vale más que un párrafo de
prosa nueva, porque se cuenta y se agrega. Si el esquema ya lo codifica, el prompt solo tiene
que **nombrarlo y decir sus cifras de hoy**.

Ver [[escribir-la-doc-de-exportacion-de-un-sistema-lo-audita-entero]].
