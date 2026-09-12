---
title: un guard que filtra a cero deja sin ejecutar el resto de la cadena
date: 2026-09-12
source: simarro
tags: [n8n, sub-workflows, gotcha]
---
En n8n un nodo con 0 items de entrada **no se ejecuta**, y arrastra consigo todo lo que cuelgue
detrás. Al meter un guard que puede devolver `[]`, lo que se cae no es solo el borrado: se cae el
`Merge`, el nodo que compone la respuesta y el `Respond`. En un sub-workflow eso se ve desde el
padre como `The workflow did not return a response` — y si el padre es un AI Agent, el modelo le
enseña ese error al cliente.

`alwaysOutputData` **no** lo arregla: solo emite el item vacío si el nodo llega a ejecutarse, y aquí
no llega. Lo que funciona es dar al Merge una entrada extra que siempre lleve dato — la propia rama
que dispara la búsqueda — para que el camino "no encontré nada" tenga salida:

    IF (rama larga) ──┬─→ Buscar → Filtrar → Eliminar → Merge#0..8
                      └────────────────────────────────→ Merge#10

Verificado 12-sep-2026 (Simarro): mismo caso, con y sin la entrada extra → `did not return a
response` vs. `{"ok":false,"mensaje":"No he encontrado ninguna visita..."}`.
Ver [[n8n-execute-workflow-nodo-terminal-ambiguo-con-multiples-ramas]] ·
[[un-borrado-encadenado-a-una-busqueda-no-puede-confiar-en-que-el-filtro-llegue]]
