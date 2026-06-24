---
title: n8n sub-workflow devuelve la última hoja; una rama paralela dead-end contamina el retorno
date: 2026-06-24
source: claude-code-session
tags: [n8n, sub-workflow, gotcha]
---
Un workflow con `executeWorkflowTrigger` devuelve a su llamador los datos de su(s) nodo(s) hoja (sin salida). Si añades una rama PARALELA dead-end (p.ej. colgar un fetch del Start para tenerlo disponible con `$('nodo').all()` aguas abajo), esa rama se vuelve una **segunda hoja terminal** y contamina el valor de retorno: el llamador puede recibir SUS datos en vez de los del nodo final.

Fix: nada de ramas paralelas dead-end en sub-workflows. Si necesitas un dato extra solo en cierto caso, ramifica con IF para que **una sola hoja produzca salida por ejecución** (bonus: el fetch solo corre cuando hace falta → menos latencia).

Caso real Simarro: "zonas cercanas" colgado del Start rompía la tool `Buscar_viviendas` (devolvía una fila del catálogo en vez de `{found,results}`). Movido a `IF found==0 → Get Catálogo → Build Zones`. Relacionado: [[n8n-nodos-compartidos-entre-ramas-requieren-if-isExecuted]].
