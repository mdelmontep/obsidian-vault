---
title: atribuir tenant ↔ entidad externa por un único campo deja huecos — unir fuentes
date: 2026-05-28
source: claude-code-session
tags: [multi-tenant, attribution, mapping, integraciones]
---

Cuando mapeas una entidad de otro servicio (otra BD, API externa) a un tenant del portal, no apoyarte en UN solo campo de atribución. El flujo real produce trazas en distintos sitios según cómo llegó cada cliente; un único filtro cubre solo uno de esos caminos.

**Caso real 2026-05-28 (agency-portal #77 → #78)**: `/documents/invoices` para Simarro solo mostraba la factura del portal. Primera versión exigía `prospects.facturaia_cliente_id` poblado para atribuir sombras direct. Ese campo solo se rellena la primera vez que el portal emite un doc para el prospect; clientes manuales o con prospect "limpio" quedaban fuera.

**Fix**: unir con `facturaia_documents.cliente_remote_id` de sombras YA enlazadas a `agency_invoices`/`invoices`/`quotes` del tenant. Si el tenant tiene cualquier emisión fiscal desde el portal, esa sombra fija el mapping.

**Regla general**: antes de elegir el filtro, listar todos los caminos por los que puede existir traza tenant↔externa. Hacer UNION de las fuentes, no elegir una. Si todas vacías → devolver vacío explícitamente ("sin atribución posible"), no fingir. Aplica a Retell/Stripe customer/Chatwoot conversation. Ver [[ADR-023-mapping-client-portal-cliente-remote-id-facturaia]] y [[helper-compartido-list-y-authz-mismo-mapping]].
