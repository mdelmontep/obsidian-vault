---
title: agh-iberica
date: 2026-07-02
updated: 2026-07-13
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

- **Borja Galván** (`notcapi`) — **autoridad de merge** + coordinación/triage; contratos compartidos (`src/domain|brain|tools`) y **dashboard CRM**.
- **Manu** (`mdelmontep`) — módulos autocontenidos del **agente conversacional** detrás de interfaz (capacidad #118, dedup #245, secretaria #467, ClientIntake #451, gaps de auditoría).
- **Dani** (`tecnocloudes`) — infra + identidad (Meta, M365/Entra, Retell, Dokploy; vínculo dashboard↔agente #489).

Reglas de no pisarse: reclamar issue antes · rama por issue → PR a `main` · avisar por Slack antes de tocar un tipo en `src/domain|brain|tools` · `git pull --rebase` a menudo.

## Stack (ADR-0001)

Cerebro en **código** (no n8n). TS. **Mastra NO adoptado en el MVP** (spike #6: canal stateless → estado en `conversation_state`; el bucle HITL es código propio detrás de la costura `Brain`; Mastra queda como puerta de salida). Servidor **Hono**. Model gateway **OpenAI-compat** (`MODEL_GATEWAY_URL`, hoy OpenAI directo — no LiteLLM; provider-agnóstico, salto a Azure-UE por config). Modelo real gpt-4o. Voz **Retell → LiveKit**. WhatsApp **Cloud API directo**. STT **gpt-4o-transcribe** (interfaz OpenAI-compatible, swap a faster-whisper). Datos **Postgres + pgvector**. Cola **Redis + BullMQ**. Observabilidad **Langfuse**. Deploy **Dokploy dedicado**. Seguridad **escalón 1** (API pública + DPA + zero-retention).

## Arquitectura

Un solo **cerebro** detrás de una costura estable: `NormalizedMessage` → `TurnResult` (`Action[]` + `OutboundMessage[]`). **Canales** = adaptadores finos. **Tools** = interfaces fakeables tenant-scoped. **Multi-tenant** (`tenant_id` + `owner_user_id`) desde el día 1. **HITL** en todo write (un HITL por turno, batch). **Recall fundamentado** (solo tools, "no consta" antes que inventar).

## Estado (2026-07-13) — PROD VIVO, secretaria conversacional completa

Demo del 7-jul con Carlos OK. CI Actions muerto por billing → **gate LOCAL** `npm run gate`/`gate:full` (lint 0-`any` + typecheck + test agente + gate dashboard [+ drift]) sobre HEAD rebasado, documentado en cada PR; **merge = Borja** (`gh pr merge --admin`, el rojo de Actions es falso negativo) o **founder override nombrando el bypass por-PR** (el clasificador lo exige; ver [[agh-self-merge-clasificador-nombrar-bypass]]). El detalle día-a-día vive en `docs/status-log/` del repo y en [[archive-completed]].

**Agente conversacional — todo en `main` + prod (autodeploy):**
- **Capacidad conversacional (épica #118)**: L1 ventana de turnos → L2a recentEntities → L2b fuente única de entidad activa + #445 anáfora a persona. Recall ~100%, OVERALL ~98-99%. **L5/L3-A POSPUESTOS por RGPD** (Borja): sin egress de nombres de cartera al LLM hasta cerrar la política de datos con el cliente.
- **Dedup de clientes #245 CERRADO**: `crm.mergeClients` (fusiona duplicados sin perder historial, transaccional) en prod + fusionado el duplicado real del drill (`grabados`→`Dragados`). Scanner read-only `scripts/scan-duplicate-clients.ts`.
- **Drill de voz #192**: 6 hallazgos mergeados (lastVoicePointer, HITL de voz, recap inventado, saludo≠siembra, puntuación ASR, sí/no desnudo).
- **Secretaria conversacional (épica #467) COMPLETA**: P1 reads de lista fraseados grounded (voz intacta, kill-switch `READ_PRESENTER_ENABLED`) + P2 social/small-talk + P5 preferencias firma/franja (`user_preferences`, mig 0016). PRs #471/#473/#474. Ver [[agh-secretaria-conversacional-plan-1-2-5]].
- **#451 `ClientIntake`** (#484): módulo único de alta (normalización + dedup exacto/aproximado 0.85 + `confirmedNew` + email→update); `CreateClientWriteExecutor`→adapter retrocompat; **onboarding gana el dedup aproximado**.
- **Gaps de la auditoría Langfuse**: #481 bucle del «sí» al conectar M365 (#494) + #482-p2 guard del `to` (no placeholder/pronombre al HITL, #491).
- **Observabilidad**: Langfuse v3 en prod (tracing activo, content=true); `userId` en claro opt-in `LANGFUSE_TRACE_PLAIN_USER_ID` (#472/#475); **rutina de auditoría semanal** (lunes 09:00, maker/checker, postea como bot; idempotente por estado de issues — ver [[audit-bot-recurrente-idempotencia-por-estado-de-issues]]).
- **Arquitectura (épica #457)**: gate raíz `npm run gate` (#453); split actor/owner (#450); `createApp` por slices en **`src/composition/`** (#455) — **wiring nuevo: tool/read/write → `capabilities.ts`, store → `persistence.ts`, env/validación → `config.ts` (⚠️ orden de throws fijado por `app-config.test.ts`), worker → `lifecycle.ts`; NUNCA `app.ts`**; smoke contra el brain real (#456, `LlmBrain` retirado).

**Dashboard CRM** (#296, Borja/Dani, prod `panel.agh.agentesialabs.com`): épica premium #392 CERRADA; escrituras en ficha (#439) + split actor/owner (#450) + CRUD de cliente completo (#305) + UI ficha/cartera (#483, mig 0017 `tasks.due_date`). En curso #490/#493 (editar/borrar notas/reuniones/tareas + pulido). Vínculo identidad dashboard↔agente vía `oid` de Entra (#489, PR #492). Zona dashboard-local, cero cruce con el agente salvo `schema.sql`.

**Migraciones al día: 0018** (`users.email`, #495). 0016 `user_preferences`, 0017 `tasks.due_date`.

**EN COORDINACIÓN (no cerrado, bloqueado en terceros):**
- **#482-p1** self-recipient «mi correo»: cimiento en prod (mig 0018 `users.email`, #495); falta el **reader** en `email-send-write-executor.ts` (espera el email poblado por **Dani** desde el token de Entra, #492) + **señal en `SYSTEM_PROMPT`** (lane Borja).
- **#485** el agente escribe `audit_log` + procedencia: **dimensionado** — el agente NO tiene write-store transaccional unificado como el dashboard → «audit en la MISMA tx» exige enhebrar `TransactionHandle` (seam #253) por el camino de escritura = contrato compartido; **espera OK de Borja al cómo**.

## Bloqueantes

- **#482-p1 / #485** — esperando respuesta de Dani (email de Entra) y Borja (señal de prompt + contrato del audit); ver arriba.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).
- **#197/#228** (agendar futuro→calendario) — scope Entra `Calendars.ReadWrite` + admin consent (Borja).
- **SSH al host de prod** con timeouts intermitentes (visto en el drill) → diagnóstico vía panel/API Dokploy mientras.
- Secrets de prod → migrar a 1Password (pendiente recurrente).

## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agentesia]] · [[top-of-mind]]
