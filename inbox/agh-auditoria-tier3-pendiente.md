---
title: AGH Ibérica — auditoría Tier 3 pendiente de ejecutar
date: 2026-07-07
tags: [inbox, agh, auditoria]
---

Prompt escrito esta sesión (no ejecutado). Tier de endurecimiento de plataforma enterprise
(RGPD/residencia UE/ISO), pistas nuevas que Tier 1 y Tier 2 no tocaron:

- **G — Persistencia & integridad de datos**: schema.sql vs realidad en BD (FKs, ON DELETE
  CASCADE a tenants, CHECK de enums, NOT NULL/UNIQUE), migraciones (forward vs HEAD, drift),
  parse-don't-validate en bordes (JSONB pending), transacciones multi-tabla.
- **H — Aislamiento multi-tenant (capa de datos) + secretos/config**: cada query scoped por
  tenant/owner (backstop by-id #47), resolvers cruzando tenant, recall pgvector scoped, RLS
  sí/no; cifrado tokens M365, secretos, fail-closed config prod (#54).
- **I — Lifecycle/recursos/observabilidad-RGPD**: cierre de pool/queue/worker en SIGTERM,
  fugas de conexión (síntoma #275), estructuras in-memory sin cota; PII en logs/trazas,
  ¿todo fallo deja traza?, health/readiness.

Mismo harness Workflow 2-fases que Tier 2, **verificando contra el esquema real** de la BD
(`pg_constraint`/`pg_policies`/`\d+`), `--maxWorkers=2`. Dedup vs cosechas Tier 1 (#252-256)
y Tier 2 (#260-268,#275). Prompt completo reconstruible desde el chat de la sesión 07-jul.
