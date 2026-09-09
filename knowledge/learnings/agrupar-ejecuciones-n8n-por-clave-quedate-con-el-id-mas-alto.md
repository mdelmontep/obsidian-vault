---
title: agrupar ejecuciones de n8n por clave de negocio pisa la medida nueva con la vieja
date: 2026-09-09
source: simarro
tags: [n8n, medicion, api]
---
Para verificar un fix disparé el webhook 14 veces y leí `GET /api/v1/executions?limit=16` +
`?includeData=true`, agrupando en un diccionario por `idealista_id` para tabular el resultado. Salió
un fallback inesperado: la ventana de 16 incluía **pruebas previas al fix** sobre las mismas
referencias, y al recorrer los ficheros por orden de `glob` (alfabético, no cronológico) la
ejecución vieja pisó a la nueva. Estuve a punto de reportar como bug del fix una medida de antes
del fix.

- Al agrupar ejecuciones por una clave de negocio, ordena por **id de ejecución ascendente** y deja
  ganar al mayor — el id de n8n es monótono; el nombre del fichero y el orden del listado no lo son.
- Síntoma que lo delata: una fila del resumen contradice lo que el nodo anterior acaba de escribir
  (aquí, `agent` poblado en el sync pero `agent_raw: null` en la RPC de la "misma" prueba).
- Barato de blindar: imprime junto a cada fila el id de ejecución del que salió. La discrepancia se
  ve sola.

Ver [[un-fallback-legitimo-hace-mudo-un-parser-incompleto]]
