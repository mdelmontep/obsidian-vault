---
title: en holded v2 el rol de un contacto es client_record/supplier_record, no type
date: 2026-07-15
source: claude-code-session
tags: [holded, integraciones, facturaia, sync]
---
El contacto de Holded v2 (`GET /contacts`) trae `type` (`client`/`supplier`/`null`)
**y además** dos sub-ledgers: `client_record` y `supplier_record` (`{num,name}` o
null). La señal FIABLE de rol es la presencia de esos records; `type` es solo la
categoría primaria y miente a menudo (63/429 con `type=null` pero con record).

**Un contacto puede ser cliente Y proveedor a la vez** (ambos records no-null).
Si el pull decide por `type` solo, mete proveedores en clientes (caso FacturaIA:
409 contactos → 0 proveedores).

Implicación de diseño en la tabla de mapeo: con `UNIQUE(org, entity_type, holded_id)`,
un contacto de doble rol necesita DOS `entity_type` (`contact_client` /
`contact_supplier`) para mapear a dos filas locales. Un único `contact` lo impide.

Gotcha extra: ampliar el union TS del `entity_type` NO basta — la BD suele tener
un CHECK constraint que hay que migrar a la vez (si no, el write falla en runtime).

Ver hub [[facturaia]] · [[facturaia-holded-integracion]] · PR #908.
