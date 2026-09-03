---
title: clientify: POST /deals ignora pipeline y un PATCH parcial reevalúa etapa y vencimiento
date: 2026-09-03
source: centro-elphis
tags: [clientify, crm, api, n8n, gotcha]
---
- `POST /v1/deals/` acepta `pipeline_stage` pero **ignora `pipeline`**: guarda el deal en el pipeline por defecto (54955) con una etapa del 56886. En la UI se ve bien y funciona… hasta el primer `PATCH` que no mande `pipeline`: 400 «Pipeline stage does not belong the pipeline» (`registrar-lead` 11666 + 10 reintentos).
- Un `PATCH` con solo `remarks` **no es parcial**: Clientify reevalúa `expected_closed_date` y, si está en el pasado, pasa el deal a `status: 2` (Expired) sin avisar.
- Patrón: (1) tras crear, PATCH de consolidación con `pipeline` + `pipeline_stage` + `status` + `expected_closed_date` (retry, sin `onError`); (2) todo PATCH manda esos cuatro campos, con vencimiento a hoy+N; (3) el body sale de un Code con `JSON.stringify`, no de expresiones sueltas por campo.
- Listar deals de un contacto: solo `?contact_id=`; `?query=` busca por nombre del deal; el listado devuelve `remarks:""`, así que fusionar notas exige el GET de detalle.
- 88 deals antiguos quedaron con pipeline 54955 + etapa 56886; decidido no hacer backfill (3-sep).
Ver [[put-objeto-completo-borra-campos-no-mapeados]] · [[clientify-discovery-elphis]] · [[ADR-079-una-reserva-de-doctoralia-mueve-todos-los-deals-abiertos-del-lead]]
