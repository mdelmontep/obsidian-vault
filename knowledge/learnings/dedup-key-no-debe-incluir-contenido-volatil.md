---
title: clave de dedup de notificaciones no debe incluir contenido volátil (contadores)
date: 2026-05-30
source: claude-code-session
tags: [frontend, ux, notificaciones]
---

Si una notificación/aviso persistente se deduplica por una clave que incluye el `message`, y ese mensaje lleva números que fluctúan ("5 emails fallidos", "Storage: 123.45 MB"), al cambiar el contador entre sondeos la clave cambia → el sistema lo trata como incidencia NUEVA → la UI reaparece aunque el usuario la haya ocultado.

Caso (TuFacturaIA, burbuja de incidencias admin): `keyOf = type:org_id:message` → ocultar no "pegaba" porque el MB de storage variaba cada poll.

Fix: la clave de identidad debe basarse en lo estable (tipo + entidad). Si necesitas distinguir por texto (p.ej. varios crons del mismo tipo), normaliza los dígitos: `message.replace(/\d[\d.,]*/g, '#')`. Así "5 emails" y "7 emails" colapsan a la misma incidencia.

**Ampliación 5-sep-2026 — normalizar los dígitos NO basta, porque las palabras también son volátiles.** El fix de arriba (`\d → #`) cerró el caso del contador y dejó abierto el resto del mensaje. Dos formas de que el texto cambie sin que cambie la incidencia: el **nombre de una org se edita** (o se fusionan dos fichas de proveedor, 31-ago), y **alguien reescribe el copy** del aviso en un PR. Las dos daban por recuperada una incidencia viva, cerraban la alerta y abrían otra con su correo.

Fix real: una bandera por alerta (`dedupe_solo_type`) que **vacía el segmento de texto** de la clave y deja `type` + entidad, para los tipos donde el `type` ya identifica la incidencia entera (cuota, VeriFactu, webhooks). El contrapeso obligatorio en el test: dos orgs distintas —y dos `type` distintos del mismo colector— tienen que seguir siendo incidencias SEPARADAS; vaciar el discriminador de más es el riesgo simétrico.

Y el test mide el **efecto** (reescribir el mensaje no cambia la clave), no que la propiedad exista: una aserción sobre la bandera pasa igual si quien construye la clave deja de leerla.
