---
title: un trabajo en cola que guarda el texto y no la referencia nace caducando
date: 2026-08-18
source: learn-agentesia
tags: [colas, jobs, arquitectura, gotcha]
---

Al encolar, el trabajo copió el enunciado ya montado (`peticion: "${t.titulo}. ${t.aprendes}…"`) en vez de resolverlo al ejecutar. Desde ese instante la cola pide **la versión de ayer**.

**Cómo se manifestó.** Se reescribieron 19 temas para quitarles la jerga del título; **16 de 20 trabajos pendientes seguían pidiendo los títulos viejos** y se habrían escrito así, deshaciendo el arreglo sin un solo error. Dos ya en vuelo salieron con el título antiguo y hubo que retirar la salida.

**Por qué no lo ves.** Nada falla: el trabajo es válido, se ejecuta, produce. Solo produce lo que se pedía antes. El desfase crece con el tiempo entre encolar y ejecutar — y una cola con horas de espera es justo donde más pasa.

**Regla.** Un trabajo diferido guarda **la referencia** (`tema_id`) y **resuelve el contenido al ejecutar**. Si guardas texto, guardas una foto.

**Si ya está encolado así**, antes de tocar la fuente: comparar cada trabajo pendiente contra su origen actual, retirar los desfasados y reencolar. Detectarlo es un `startswith` del título.

Ver [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] · [[antes-de-arreglar-lo-que-viste-en-un-log-mira-contra-que-version-paso]]
