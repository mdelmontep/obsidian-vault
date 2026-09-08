---
title: sin filtro por campo personalizado, una importación masiva solo es reanudable por request_id
date: 2026-09-09
source: simarro
tags: [kommo, crm, importacion, idempotencia]
---
Plan inicial para meter 2.616 contactos en Kommo: "antes de cada tanda, consulto qué referencias ya
existen". No funciona: **la API v4 no tiene filtro por campo personalizado**. Solo hay `query`, que
es búsqueda de texto libre sobre todo el contacto — no discrimina "el CF Ref. origen vale X".
Si la carga se corta a mitad, no hay forma fiable de saber por dónde iba.

Lo que sí funciona: cada entidad del POST lleva `request_id` = su clave natural del origen. Kommo lo
devuelve junto al id creado, así que **tras cada lote se persiste el mapeo `ref → id` en fichero**, y
ese fichero —no una consulta al CRM— es la fuente de qué queda pendiente.

Agrava el asunto que Kommo **no deduplica al crear por API** (su control de duplicados es solo para
leads entrantes) y que **no deja borrar contactos**: `DELETE` individual y en bloque devuelven 405,
comprobado en vivo. Un lote mal enviado se limpia a mano en la UI, uno a uno.

Regla: en una carga masiva contra un CRM, la idempotencia se lleva en **tu** fichero de avance, no
en una consulta al destino. Solo delega en el destino si tiene filtro exacto por la clave natural.
