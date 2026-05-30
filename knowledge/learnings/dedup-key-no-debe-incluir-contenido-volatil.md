---
title: clave de dedup de notificaciones no debe incluir contenido volátil (contadores)
date: 2026-05-30
source: claude-code-session
tags: [frontend, ux, notificaciones]
---

Si una notificación/aviso persistente se deduplica por una clave que incluye el `message`, y ese mensaje lleva números que fluctúan ("5 emails fallidos", "Storage: 123.45 MB"), al cambiar el contador entre sondeos la clave cambia → el sistema lo trata como incidencia NUEVA → la UI reaparece aunque el usuario la haya ocultado.

Caso (TuFacturaIA, burbuja de incidencias admin): `keyOf = type:org_id:message` → ocultar no "pegaba" porque el MB de storage variaba cada poll.

Fix: la clave de identidad debe basarse en lo estable (tipo + entidad). Si necesitas distinguir por texto (p.ej. varios crons del mismo tipo), normaliza los dígitos: `message.replace(/\d[\d.,]*/g, '#')`. Así "5 emails" y "7 emails" colapsan a la misma incidencia.
