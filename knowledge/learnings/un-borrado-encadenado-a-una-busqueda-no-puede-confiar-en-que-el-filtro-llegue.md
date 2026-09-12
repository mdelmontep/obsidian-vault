---
title: un borrado encadenado a una búsqueda no puede confiar en que el filtro llegue
date: 2026-09-12
source: simarro
tags: [n8n, google-calendar, produccion, fail-closed]
---
`getAll` + `delete` en cadena es una escopeta: si el filtro evalúa a vacío, el `getAll` devuelve
**todo** y el `delete` lo borra todo. En n8n el filtro llega como expresión (`{{ $json.Lead_id }}`),
y una rama que cambia el item de entrada la deja en `undefined` **sin error** — la query se envía
vacía y Google responde con el calendario entero. Caso real 12-sep-2026 (Simarro): una rama de
cancelación recibía el item de otro nodo, sin `Lead_id`; 10 citas reales de 4 agendas borradas en
una sola ejecución. Bug latente desde siempre, invisible mientras los leads sí traían el dato.

Regla: entre buscar y borrar va **un nodo que reafirme la pertenencia** con el dato leído de su
nodo de origen (`$('Nodo').first().json.x`), no del `$json` que arrastre la rama:
- sin identificador válido → `return []`, nunca "borra lo que haya salido";
- el filtro se comprueba contra el contenido del propio recurso (`Lead ID: <id>` en la description),
  no contra la promesa de que el buscador filtró.

Y el guard cambia el flujo: si deja 0 items, el nodo siguiente no corre → hay que dar salida
explícita al caso "no encontré nada". Ver [[un-guard-que-filtra-a-cero-deja-sin-ejecutar-el-resto-de-la-cadena]] ·
[[google-calendar-query-busca-en-summary-y-description]]
