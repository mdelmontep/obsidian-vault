---
title: antes de exceptuar una deuda, mira qué trinquete la mide
date: 2026-09-04
source: facturaia
tags: [gates, ratchets, deuda-tecnica, auditorias]
---
Un cierre dejó «9 hallazgos `side-tab` en las plantillas: decidir si excepción de dominio». Al ir a
concederla, dos hechos la desmontaron:

1. **El gate no medía eso.** `design-debt-ratchet` cuenta `buttons`, `hex` y `nativos`; `borderLeft`
   no es métrica suya. Exceptuarlo obligaba a inventar un contador cuyo único acto fuese no contar,
   y dejaba un `isXExcluded` que el siguiente lector lee como precedente para sacar la carpeta.
2. **Ya estaban capados por OTRO trinquete**: `inline-style-ratchet`, sin exclusiones, techa esas
   plantillas (99/89/76) y cada `borderLeft` vive dentro de un `style={` contabilizado.

Regla: ante «declaremos una excepción», primero grep de qué script mide de verdad el patrón. Si
ninguno, no hay nada que exceptuar; si otro sí, sobra. Y ampliar una exclusión que ya existe de
**fichero** a **carpeta** regala lo que sí era migrable (aquí 23 hex de bloques compartidos).

La etiqueta de un agente auditor no es un identificador grepeable: arrastrarla como «pendiente»
costó una vuelta de arqueología. Ver [[una-lista-de-hallazgos-caduca]].
