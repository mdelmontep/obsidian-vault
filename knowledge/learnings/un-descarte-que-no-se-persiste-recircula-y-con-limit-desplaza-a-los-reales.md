---
title: un descarte que no se persiste recircula, y con LIMIT desplaza a los casos reales
date: 2026-09-09
source: clinica-zen
tags: [n8n, sql, cron, batch, dedupe]
---
Un job periódico que SELECCIONA candidatos, los filtra con una comprobación cara (una llamada a la
API del CRM) y solo apunta en la tabla de dedupe los que **sí** ejecutó, vuelve a traerse los
descartados en cada pasada. Con un `LIMIT N` en la consulta —y peor sin `ORDER BY`— esos descartes
perpetuos copan el lote y **los casos reales dejan de evaluarse**. Es el fallo original disfrazado.

Medido: gate de reenganche cada 30 min, `LIMIT 5`, la misma sesión en 4 ejecuciones seguidas. Con 5
conversaciones bien cerradas en 24 h, cero abandonos reales atendidos.

Reglas: **persistir el descarte igual que el envío** (el `NOT EXISTS` ya se invalida solo cuando el
usuario vuelve a escribir), poner `ORDER BY` a cualquier `LIMIT`, y **leer el CHECK antes de
inventarse un `status`** — esquivar el constraint dejando de escribir fila es lo que creó esto.

No lo cazan los tests de la decisión ni un smoke de una pasada: los dos miran «¿hizo lo correcto
ahora?». La pregunta que discrimina es **qué pasa en la pasada SIGUIENTE**.
Ver [[reenganche-por-ultimo-mensaje-del-bot-dispara-tambien-en-conversaciones-bien-cerradas]] · [[clinica-zen]]
