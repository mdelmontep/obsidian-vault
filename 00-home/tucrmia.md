---
title: TuCRMIA
updated: 2026-08-02
tags: [hub, tucrmia, crm]
---

# TuCRMIA — hub

CRM conversacional de AgentesIA. **Módulo activable de una plataforma**, con app y base propias.
Repo `AgentesIA-MAdrid/tucrmia` · local `~/Projects/agentesia-crm`.

**El contexto vive en el repo, no aquí.** Este hub es solo el índice desde el vault:
- `CLAUDE.md` — reglas y contexto que no se deduce del código. Se lee primero.
- `docs/plan/ESTADO.md` — progreso. **Fuente de verdad.**
- `docs/plan/PROMPT-CONTINUACION.md` — cómo retomarlo en otra sesión.

## Estado (02-ago, tarde)

- **F0: 6 issues cerrados de 16.** Gate con **14 comprobaciones y 205 tests**, más `npm run db:replay`
  contra un Postgres 17 real en Docker. Desplegado: `/api/health` responde el commit de `origin/main`.
- **005 cerrado**, con los seis criterios verificados y no supuestos, incluido el plan de ejecución medido
  con 200.000 filas. Auditado después con cinco lentes adversariales: encontraron **una fuga entre clientes
  en la `001`, que ya estaba aplicada**, y un fallo que habría impedido aplicar la `002`. Las dos cerradas,
  la fuga con un test que se pone rojo sin el arreglo.
- Plan salido de 28 agentes + 3 críticos: 77 épicas en 5 fases. El hito que importa es **F2**, cuando el
  inbox sustituye a Kommo.
- Siguiente: issue **006**, el disparo trazador de la API pública.

## Bloqueos

- 🔴 **El token de la Management API de Supabase.** Es lo único que separa el 005 de estar en producción:
  `SUPABASE_ACCESS_TOKEN=$(op read "op://…") node scripts/apply-migration.mjs --check`. El procedimiento ya
  no es tácito (aplica y registra la versión en la misma transacción); falta de dónde sale el token.
- 🟠 **Antes del issue 006**: decidir si el recurso `webhook` del catálogo se parte en `integration`. De ahí
  se derivan los scopes de la API pública y un scope publicado es contrato con clientes.
- 🟠 Sesión de diseño (índigo exacto, densidad, 4 pantallas) → bloquea issues 009 y 011.
- 🟠 Registrar `tucrmia.com`, App Review y Access Verification de Meta → bloquean F2, no antes.

## Decisiones

- `ADR-001` — sin número de WhatsApp compartido: capacidades W0 (sandbox por org) y W2 (canal dedicado).
- `ADR-002` — es un módulo activable de una plataforma: alta, login y cobro dejan de ser nuestros.
- `ADR-003` — el CRM **no cobra**. Cierra P21, que ya no bloquea F1.

## Learnings de este proyecto

[[test-de-equivalencia-entre-artefactos-generados-es-tautologia-sobre-la-definicion]] ·
[[el-entorno-de-un-test-que-evalua-sql-emitido-no-se-escribe-a-mano]] ·
[[replay-de-migraciones-contra-un-postgres-desechable-en-docker]] ·
[[rls-multi-org-active-vs-membership]] ·
[[pooler-supabase-inalcanzable-aplicar-migracion-por-management-api]] ·
[[pipe-a-tail-enmascara-el-exit-code-del-comando]] ·
[[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]] ·
[[dig-ns-vacio-no-significa-que-el-dominio-este-libre]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
