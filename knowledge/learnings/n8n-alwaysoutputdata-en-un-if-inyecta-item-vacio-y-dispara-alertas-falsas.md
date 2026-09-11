---
title: `alwaysOutputData: true` en un nodo IF inyecta un item vacío y dispara alertas falsas
date: 2026-09-08
source: clinica-zen
tags: [n8n, if, alertas, falsos-positivos, gotcha]
---

Con `alwaysOutputData: true` en un **nodo IF**, cuando una de sus salidas se queda sin
items n8n **inyecta un item vacío `{}` por la salida 0**. Si de esa salida cuelga una
alerta, la alerta se dispara **en cada ejecución** con todos los campos a `undefined`.

Caso real (Clínica Zen): un guard que vigilaba si el chatbot anunciaba una cita sin
reservarla mandó **5 falsos positivos a Slack** —
`lead=undefined | frase: undefined | sonda: undefined` — mientras el Code node que lo
alimentaba funcionaba perfectamente. El bug no estaba en la lógica, estaba en la opción.

**Dónde sí es correcto** `alwaysOutputData`: en un **Code node** o en un **getAll de
Google Calendar**, donde quieres que el flujo continúe con 0 resultados — pero **solo si el
nodo de abajo filtra el item vacío**; si no, cambias una rama muda por un crash en cada pasada
(11-sep, Laserys: 23 ejecuciones seguidas en rojo). Ver
[[n8n-gcal-getall-empty-no-propaga-downstream]]. En un **IF** es un generador de
ruido: el IF ya tiene dos salidas, no necesita placeholder.

## Reglas accionables

1. **Nunca `alwaysOutputData` en un IF.**
2. Resolver el booleano **dentro de la expresión**: `={{ $json.alerta === true }}` en
   vez de `={{ $json.alerta }}`. Así un valor ausente cae en la rama falsa, en lugar de
   provocar un error de tipo que —con `onError: continueRegularOutput`— sale por la
   **salida 0**, justo la de la alerta.

Relacionado: [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]] ·
[[n8n-cierra-la-expresion-en-el-primer-doble-llave-y-trunca-el-jsonbody]]
