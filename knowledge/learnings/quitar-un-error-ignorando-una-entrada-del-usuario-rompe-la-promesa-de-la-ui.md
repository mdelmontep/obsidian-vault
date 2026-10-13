---
title: quitar un error ignorando una entrada del usuario rompe la promesa de la ui
date: 2026-10-13
source: agh-iberica #2493 (RRHH, sustitución borrador → firmado)
tags: [ux, validacion, revision-adversarial, hitl]
---
**Qué pasó:** con «este firmado sustituye al borrador» marcado y la fecha de inicio corregida en el mismo lote, el servidor daba un 409 sin explicación. Mi primer arreglo **ignoraba la casilla**: se guardaba, y el gate, los tests y la mutación salían en verde. Pero la casilla prometía «el borrador dejará de ser el vigente al guardar», y el borrador seguía vigente en silencio.

**Patrón:** cuando dos entradas del usuario se contradicen (aquí «es el mismo contrato» y «empieza otro día»), descartar una para que el error desaparezca convierte un fallo visible en un dato falso. El texto de la UI que pidió esa entrada pasa a mentir.

**Fix:** un error **tipado** que nombra la contradicción y deja elegir (mantener la fecha o desmarcar la casilla), visible ya en la preview. El 409 se queda solo para la carrera real, es decir, cuando el estado cambió por debajo.

**Detector:** al revisar un arreglo de un error, pregunta qué le prometió la UI al usuario por la entrada que el arreglo ignora. Lo cazó una revisión con contexto limpio obligada a leer la UI, no la mía ([[agh-iberica]]).
