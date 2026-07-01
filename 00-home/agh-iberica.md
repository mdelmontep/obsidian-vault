---
title: agh-iberica
date: 2026-07-02
updated: 2026-07-02
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

## Estado (2026-07-02)

- ✅ **#4** esqueleto andante (LlmBrain + gateway + whitelist multi-tenant + webhook WhatsApp + Postgres) — mergeado (abierto para end-to-end en vivo, bloqueado por #1).
- ✅ **#6** bucle HITL proponer→confirmar→ejecutar + primera entidad CRM (Cliente) — mergeado (PR #20).
- ✅ **#15 (STT)** `TranscriptionProvider` + `gpt-4o-transcribe` (Manu) — mergeado (PR #18).
- 🔵 **#9 (M365)** OAuth con PKCE + state cifrado + tokens cifrados (AES-256-GCM/HKDF) + `CalendarTool` "¿qué tengo hoy?" (Europe/Madrid) + Postgres cifrado (Manu) — **PR #21 abierto, en review**.
- ⏳ CI en GitHub Actions; `main` protegido (PR + check `test` verde obligatorio).

**Ruta crítica:** `#1 → #4 → #5 → #6 → #7`. Tras #6, fan-out: #8, #11, #9→#10, #13, #14.

## Bloqueantes

- **#1 WhatsApp/Meta** (número + credenciales) — Dani. Desbloquea end-to-end WhatsApp.
- **#2 M365** (app registration Entra ID: `Calendars.Read` + `Mail.Send`, tenant de prueba propio de AIA) — desbloquea el end-to-end del #9/#10.
- **#3 Retell** (API key por 1Password) — desbloquea #13.
- **Dokploy dedicado** — producción, no bloquea desarrollo.
- **CI parada**: GitHub Actions dejó de encolar runs (probable límite de minutos/facturación de la org `AgentesIA-MAdrid`) → con `main` protegido, bloquea todos los merges. Revisar Settings → Billing.

## Cabo abierto de integración (#6 ↔ #9)

El `CalendarTool` del #9 está listo y testeado, pero el brain aún **no lo enruta**: `TurnInterpretation.read` solo admite `target: "clients"` y `HitlBrain` tiene `ClientStore` hardcoded. Para que "¿qué tengo hoy?" funcione por chat hay que extender la costura del brain (intención de calendario + inyectar el tool). **No estaba en PRD ni issues** — avisado a Borja + anotado en PR #21.

## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agentesia]] · [[top-of-mind]]
