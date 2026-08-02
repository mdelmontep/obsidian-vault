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

## Estado (02-ago)

- **F0: 5 issues cerrados de 16.** Gate con 9 comprobaciones y 29 tests. Desplegado y verificado:
  `/api/health` responde el commit de `origin/main`.
- Plan salido de 28 agentes + 3 críticos adversariales: 77 épicas en 5 fases. El hito que importa es **F2**,
  cuando el inbox sustituye a Kommo.
- Siguiente: issue 005, autorización única (decisión irreversible A8).

## Bloqueos

- 🔴 **P21 — quién cobra el módulo y cómo se reparte.** Bloquea F1.
- 🟠 Sesión de diseño (índigo exacto, densidad, 4 pantallas) → bloquea issues 009 y 011.
- 🟠 Registrar `tucrmia.com`, App Review y Access Verification de Meta → bloquean F2, no antes.

## Decisiones

- `ADR-001` — sin número de WhatsApp compartido: capacidades W0 (sandbox por org) y W2 (canal dedicado).
- `ADR-002` — es un módulo activable de una plataforma: alta, login y cobro dejan de ser nuestros.

## Learnings de este proyecto

[[pooler-supabase-inalcanzable-aplicar-migracion-por-management-api]] ·
[[pipe-a-tail-enmascara-el-exit-code-del-comando]] ·
[[traefik-me-no-emite-certificado-por-cupo-compartido-agotado]] ·
[[dig-ns-vacio-no-significa-que-el-dominio-este-libre]]

## Trampas conocidas

- El **pooler de Supabase no va desde la red habitual**: migraciones por Management API **registrando la
  versión a mano**.
- `application.one` de Dokploy **devuelve los secretos en claro**; usar `dokploy-safe.sh`.
- Mientras la URL sea HTTP, **sin datos reales de clientes**.
