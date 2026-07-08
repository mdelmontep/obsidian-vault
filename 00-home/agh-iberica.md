---
title: agh-iberica
date: 2026-07-02
updated: 2026-07-08
tags: [cliente, agh-iberica, agente-comercial, mastra, m365, whatsapp, multi-tenant, HUB]
---

# AGH Ibérica — agente comercial "Carlos"

HUB del proyecto. Empresa de IT que da servicio a grandes multinacionales (Dragados, McDonald's, aseguradoras). Quieren que **AIA agentesIA sea su departamento de IA**. Modelo: AGH = prime contractor / canal comercial; **AIA = brazo de delivery**. Todo lo construido debe ser **empaquetable y reutilizable** para que AGH lo revenda.

**Contacto:** Carlos (CEO de AGH Ibérica España).

## Producto en curso: agente comercial "Carlos"

Agente conversacional **interno** (secretario/CRM) para los propios comerciales de AGH. Primera versión/demo que testeará el propio Carlos. Se habla por **WhatsApp (voz in / texto out)** y **llamada de voz (Retell)**.

Clave: **no tienen CRM → el agente ES el CRM**. Registra por voz clientes, contactos, oportunidades (embudo) y consultores; hace recall fundamentado ("¿qué me pidió Dragados?" con fecha), lee agenda M365, manda emails de recap, gestiona tareas/recordatorios. Todo write pasa por **HITL** (proponer→confirmar→ejecutar).

Se construye como **rebanada vertical de una plataforma multi-tenant**: `base + rol-pack (comercial) + vertical-pack (AGH/staffing IT) + tenant-manifest`. AGH es el cliente nº1; reutilizable en clínicas/pymes cambiando config.

> Diferencia vs resto de clientes AIA: cliente final **multinacional**, no pyme. Back-office, su stack (M365/SAP/Salesforce), POCs con KPIs, compliance (RGPD, residencia UE, ISO), ciclos largos.

## Enlaces

- **Repo:** `AgentesIA-MAdrid/agh-iberica` (privado) — GitHub Issues como tracker.
- **Slack:** canal `#cli-agh-iberica` (`C0BEL4Q0NRY`) · canvas índice del proyecto fijado en el canal (apunta, no copia).
- **Docs en repo:** `docs/PROJECT-STATUS.md` (punto de entrada de cada sesión), `docs/PRD-agente-comercial-carlos.md`, `docs/adr/0001-stack-mvp.md`.
- **Carpeta local de trabajo:** `~/AGH Iberica`.

## Equipo y reparto

- **Borja Galván** — conduce la **espina** `#4 → #5 → #6` (define los contratos compartidos: `src/domain|brain|tools`) + `#14`.
- **Manu** — **módulos autocontenidos detrás de interfaz** en paralelo (sin pisar la espina): #15 STT, #9 M365.
- **Dani** — setups externos (Meta, M365, Retell, Dokploy).

Reglas de no pisarse: reclamar issue antes · rama por issue → PR a `main` · avisar por Slack antes de tocar un tipo en `src/domain|brain|tools` · `git pull --rebase` a menudo.

## Stack (ADR-0001)

Cerebro en **código** (no n8n). TS. **Mastra NO adoptado en el MVP** (spike #6: canal stateless → estado en `conversation_state`; el bucle HITL es código propio detrás de la costura `Brain`; Mastra queda como puerta de salida). Servidor **Hono**. Model gateway **LiteLLM** (provider-agnóstico, salto a Azure-UE por config). Voz **Retell → LiveKit**. WhatsApp **Cloud API directo**. STT **gpt-4o-transcribe** (interfaz OpenAI-compatible, swap a faster-whisper). Datos **Postgres + pgvector**. Cola **Redis + BullMQ**. Observabilidad **Langfuse**. Deploy **Dokploy dedicado**. Seguridad **escalón 1** (API pública + DPA + zero-retention).

## Arquitectura

Un solo **cerebro** detrás de una costura estable: `NormalizedMessage` → `TurnResult` (`Action[]` + `OutboundMessage[]`). **Canales** = adaptadores finos. **Tools** = interfaces fakeables tenant-scoped. **Multi-tenant** (`tenant_id` + `owner_user_id`) desde el día 1. **HITL** en todo write (un HITL por turno, batch). **Recall fundamentado** (solo tools, "no consta" antes que inventar).

## Estado (2026-07-08) — PROD VIVO, post-demo en marcha

Demo del 7-jul con Carlos **pasó bien**. CI de GitHub Actions muerto por billing de la org (no se paga) → gate = local (lint+typecheck+vitest sobre BD real 5433/6380) documentado en cada PR, merge con `gh pr merge --admin` (o desde la UI web si la cuenta no tiene admin del repo — ver [[github-required-check-failing-bloquea-incluso-admin-merge]]).

**Sesión maratón 7/8-jul (tren de merges + Fase 2):**
- ✅ **Tren de merges completo**: 15 PRs → `main`, 0 abiertas de la sesión. Encontrado y arreglado symlink `node_modules` colado a main por error propio (worktree).
- ✅ **Tier 3 completo** (auditoría adversarial, 4 grupos, #284-#290): trazar writes fallidos en Langfuse, idempotencia del confirm HITL, traza de outbound cross-canal, funnel per-tenant real + dedup de import CSV + `UNIQUE` en `clients` (migración 0007).
- ✅ **Voz pre-demo 7/9**: #232 (pending no secuestra conversación), #241 (recall ya no crea reunión duplicada), #231 (deletreo solo en altas nuevas), #246 (teléfono dictado en palabras ya no se pierde + backstop), #233 (grounding de reads), #237 (resolución de referencias parcial/difusa), #242 (capacidades no se derivan a WhatsApp de más). Todos con EVALS reales ×3 (key OpenAI provista en sesión, guardada en `.env` local, NUNCA committeada).
- 🟡 **Deferred con análisis en el issue** (no a medias): #228 (agendar futuro→calendario M365) necesita `CalendarWriteExecutor` que no existe, depende de #197. #247 (subconjunto de lista tras pointer) necesita estado conversacional nuevo (`lastVoicePointer`) que atraviesa casi todo `hitl-brain.ts` — mejor con la épica #118. #238 (lectura natural de fecha/hora) necesita cambiar la firma de `WriteExecutor.summarize()` para conocer el canal (7 executores + call sites) — refactor real, no fix puntual.
- ✅ **Voz resto COMPLETO (mismo día, 2ª mitad de sesión)**: #234 (TTL pending 1h→1 semana, parcial: "no anunciar al arrancar" queda documentado, necesita `isCallStart` + decisión de producto de Borja), #240 (enumerar tipos de alta), #239 (email hablado con pausas «arroba»/«punto»), #202 (tono secretaria en voz para un solo write; batch multi-write mantiene formato por-línea a propósito, ver [[voz-batch-multi-write-no-fusionar-en-una-frase-rompe-deletreo-dosificado]]), #191 (leer buzón responde honesto, no clarify en bucle), #204 (compromiso con marco temporal en reunión propone también task/reminder), #236 (intent "repeat" nuevo — «¿repite?» re-dice lo último sin persistencia nueva), #235 (consultor inexistente en addCandidate inyecta su alta como prerequisite del mismo batch, ver [[hitl-prerequisite-injection-colapsa-dialogo-multi-turno-de-intencion-compuesta]]), #245 (parcial: salida "es nuevo" del dedup #227 ya no repregunta en bucle vía `confirmedNew`; quedan items 2-5 — merge/delete duplicados, limpieza prod — documentados en el issue, sin cerrar). 9/9 con PR propia + gate local verde (1088→1104 tests) + EVALS ×3 donde tocaba prompt.
- 🔴 **Pendiente próxima sesión**: #150 (vitest 2→4 + typescript 6, major bump post-demo, no trivial — worktree aislado + suite completa como red), Fase 3 (triaje del resto sin tocar código, excluir #295-#309 del dashboard) y Fase 4 (cierre: reescribir `docs/PROJECT-STATUS.md` a la realidad + cerrar/comentar issues resueltos que falten).
- **Dashboard CRM** (proyecto PARALELO de Borja/Dani, PRD #295): zona 100% fría `dashboard/` — auth+OIDC Entra, cartera+VisibilityPolicy, ficha+timeline, gestión usuarios, todo YA en `main` y en prod (`panel.agh.agentesialabs.com`). Cero cruce con el agente salvo `schema.sql` (migraciones 0006 Borja, mías 0007, próxima suya 0008+ para `audit_log`).

**Ruta crítica del MVP conversacional**: completa desde hace semanas. Todo el trabajo actual es hardening post-demo + backlog de voz.

## Bloqueantes

- **#263** (dedup Retell) bloqueado por zona compartida con #258 (ya resuelto, revisar si sigue bloqueado).
- **#197/#228** — necesitan scope Entra `Calendars.ReadWrite` + admin consent (Borja).
- Secrets de prod → migrar a 1Password (pendiente recurrente).

## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agentesia]] · [[top-of-mind]]
