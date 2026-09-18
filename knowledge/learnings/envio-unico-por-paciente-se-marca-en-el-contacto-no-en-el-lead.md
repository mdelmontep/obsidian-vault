---
title: un envío «una sola vez por paciente» se marca en el contacto, no en el lead
date: 2026-09-18
source: clinica-zen
tags: [kommo, crm, idempotencia, n8n]
---

El lead es efímero: el mismo paciente vuelve a pedir cita y nace otro lead. Si la marca de «ya
enviado» (etiqueta, campo, fila) vive en el lead, el segundo lead vuelve a disparar el envío. La
identidad estable es el CONTACTO.

Patrón usado en la valoración post-cita de Clínica Zen (`sa3W3r6WfVoV9sd9`):
- etiqueta `Valoración solicitada` en el contacto = marca permanente, y quitarla es el «reenviar» manual;
- `INCR` en Redis con TTL por contacto = candado corto contra dobles disparos mientras se espera;
- re-lectura del lead y del contacto DESPUÉS de la espera, antes de enviar.

Kommo acepta `tags_to_add` en `PATCH /api/v4/contacts` igual que en leads, así que la marca no
necesita campo propio.
