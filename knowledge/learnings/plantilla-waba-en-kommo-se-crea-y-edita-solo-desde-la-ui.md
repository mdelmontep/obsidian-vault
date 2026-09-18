---
title: la plantilla waba de kommo se crea y se edita solo desde la ui, y la variable puede quedar como texto
date: 2026-09-18
source: clinica-zen
tags: [kommo, whatsapp, plantillas, api]
---

`POST /api/v4/chats/templates` crea la plantilla, pero **no sirve para ponerla en producción**:
`waba_selected_waba_ids` se ignora (llega y vuelve `[]`, con PATCH, como string y como int), y sin
cuenta WABA asociada `POST .../{id}/review` devuelve 200 con `reviews: []` — no modera nada. Una
plantilla ya aprobada tampoco se edita: el PATCH responde `EntityNotFound` aunque el GET la devuelva
con `is_editable: true`. Para cambiar una aprobada, plantilla nueva y repuntar el bot que la envía.

Y al crearla en la UI, la variable puede guardarse como TEXTO: la vista previa pinta `[Manu]` en los
dos casos, así que a ojo son idénticas. Se distingue por API: la buena trae `{{contact.name}}` en
`content` y `waba_examples` con valores; la rota trae `[Manu]` literal y `waba_examples: []`.
Comprobar SIEMPRE por API antes de mandarla a aprobar — aprobada ya no se corrige.

Útil: `GET /api/v4/chats/templates?with=reviews` trae `review_status` (approved/review/rejected) de
todas; así se ven las rechazadas por Meta que nadie mira.
