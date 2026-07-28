---
title: kommo salesbot/run exige entity_type entero — con "2" devuelve 400 siempre
date: 2026-07-28
source: claude-code-session
tags: [kommo, salesbot, n8n, clinica-zen]
---
`POST /api/v2/salesbot/run` valida el TIPO de `entity_type`: entero. Con la cadena `"2"`
responde `400 {"errors":{"error":"Invalid field: entity_type"},"detail":"Some parameters
incorrect..."}` — un mensaje genérico que no señala el campo hasta que lees la clave `errors`.
La doc oficial (developers.kommo.com/reference/launch-salesbot) no publica el schema del body.

Sonda segura para diagnosticarlo sin enviar mensajes a nadie: llamar con un `entity_id`
INEXISTENTE. Si el tipo es correcto llega a la comprobación de entidad y da `403 Entity not
found`; si el tipo es incorrecto muere antes con el 400. La respuesta distingue las dos capas.

Caso real (Clínica Zen): dos nodos de recordatorios con `"entity_type": "2"` llevaban desde
su creación fallando el 100% de los envíos, mientras otros 13 nodos del mismo sistema usaban
entero y funcionaban. Nadie lo vio porque el dedup marcaba "enviado" antes de enviar.
Ver [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]] · [[clinica-zen]]
