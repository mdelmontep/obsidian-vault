---
title: ADR-044 — una sola tabla de contactos para toda la app, no una por módulo
date: 2026-07-29
status: aceptada
tags: [adr, facturaia, arquitectura, obras]
---

**Contexto.** El ticket #96 pedía varias personas de contacto por cliente. El módulo Obras ya
tenía las suyas (`obras_contactos`, mig 475), colgadas de una *delegación*, no del cliente.

**Alternativas reales.**
1. `clientes_contactos` nueva conviviendo con `obras_contactos`, con un botón "copiar a la ficha".
   Riesgo cero de regresión en Obras, que está en producción.
2. Tabla única `contactos` (cliente XOR proveedor, `delegacion_id` opcional), migrando las de Obras.

**Decisión: la 2.** Para un instalador, Javi es a la vez el jefe de obra de una sede y la persona
a la que manda la factura; con dos tablas hay que explicarle una distinción que no tiene en la
cabeza. Y "copiar" congela el dato: cambias su móvil en Obras y la factura sigue saliendo con el
viejo, que es justo la queja del ticket.

**Cómo se neutralizó el riesgo de la 1.** El backfill conserva el `id` de cada contacto, así que
las FKs de `obras_presupuestos`/`obras_pedidos` se repuntan sin tocar una sola fila de documentos.
Expand/contract: `obras_contactos` se congela, no se dropea, hasta que la nueva lleve tiempo
rodando. Baja lógica, porque el contacto queda impreso en documentos que se regeneran.

**Coste asumido.** Una sola puerta de alta (la ficha del cliente), lo que cambia una pantalla que
el usuario ya usaba. Migs 583/585/586. Ver [[fk-compuesta-on-delete-set-null-anula-todas-las-columnas]].
