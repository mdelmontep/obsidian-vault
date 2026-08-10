---
title: un workflow activo no significa que alguien lo llame — grep su id antes de editarlo
date: 2026-08-10
source: claude-code-session
tags: [n8n, metodo, elphis]
---
Edité `notify-cita-confirmada-email` (Elphis) para que los correos fueran al cliente en vez de a
mi buzón de staging: PUT 200, checks verdes, cero efecto. **Nadie lo llama.** El rediseño de junio
(el paciente elige hueco en Doctoralia) dejó `book-and-notify` sin nodo de reserva ni de email, y
el sub-workflow quedó huérfano — activo, sin ejecuciones, invisible como problema.

La pista estaba antes de editar: `book-and-notify` con 5 ejecuciones en `success` y el
sub-workflow con **0** en el mismo periodo. Un padre en verde no prueba que el hijo corriera.

**Antes de editar un sub-workflow**, dos comprobaciones de 10 segundos contra la BD de n8n:
```sql
select id, name from workflow_entity where nodes::text like '%<ID_DEL_SUB>%';  -- ¿quién lo llama?
select count(*) from execution_entity where "workflowId"='<ID_DEL_SUB>';        -- ¿corre?
```
Cero filas en la primera = huérfano; editarlo es tiempo perdido y una falsa sensación de arreglo.
Al terminar, desactivarlo: dejarlo activo garantiza que el siguiente repita el error.

Primo hermano, mismo cliente y misma familia de fallo un nivel más abajo (rama en vez de
workflow): [[canal-nuevo-en-workflow-no-hereda-los-side-effects-de-la-rama-original]].

Ver [[n8n-status-success-no-implica-camino-critico]] · [[nodo-huerfano-puede-estar-desconectado-porque-otro-mecanismo-ya-lo-cubre]] · [[cron-endpoint-retirado-deja-schedule-externo-huerfano]]
