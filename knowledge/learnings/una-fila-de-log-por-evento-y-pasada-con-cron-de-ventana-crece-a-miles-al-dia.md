---
title: una fila de log por evento y pasada con cron de ventana crece a miles al día
date: 2026-08-24
source: agency-portal
tags: [cron, logs, postgres, volumen, flota-ia]
---
Tabla de logs "una fila por evento procesado" + cron que reprocesa una ventana deslizante = crecimiento lineal con el número de pasadas, no con el tráfico.

Cifra real (Flota IA, 24-ago): 50 llamadas/día, ventana 48 h, cron cada 15 min → ~100 llamadas en ventana × 96 pasadas = **~9.600 filas/día, 3,5 M/año**, sin que nadie las lea (solo psql). El legacy escribía UNA fila-resumen por corrida y por eso no se vio venir.

Fix en dos capas:
- **Corto-circuito `unchanged`**: si la entidad ya está cerrada y completa (`ready_to_judge`), no reescribir ni loguear; solo tocar `last_event_at`.
- **Purga** colgada del cron diario que ya existe (`received_at < now() - 30 d`, en lotes), devolviendo el recuento en la respuesta.

Al diseñar cualquier `*_ingest_logs`: estimar filas/día = (eventos en ventana) × (pasadas/día), no eventos/día. Si nadie va a leer la tabla desde la UI, decirlo en la migración y dar la consulta psql de operación.
