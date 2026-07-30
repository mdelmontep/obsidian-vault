---
title: agh-iberica
date: 2026-07-02
updated: 2026-07-30
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

## Estado (2026-07-30, noche) — Fase 0 y P1 EN PROD, 3 PRs vivas, y lo que queda ya no es mío

**`main` en `492bb13`.** Borja mergeó hoy los dos trenes + su tanda de staffing (#661/#662/#660, migs 0024-0027). **En prod del plan de precisión: Fase 0 (#531, el termómetro) y P1 (#681, el scoping de compilación).**

**Mías abiertas y MERGEABLES sobre `main`:** **#688** (#687, Fase 1 mitad de código: `RemindersReadTool` + `OpenThreadsReadTool` + filtros por cliente/estado de `TasksReadTool`) · **#692** (#691, P2: el guard de clasificación del presentador) · **#695** (docs del cierre + `dump.rdb` a `.gitignore`).

**Lo que queda del plan está bloqueado por decisiones ajenas, no por trabajo:**
- **#689** — mitad de prompt de la Fase 1 (una línea por tool en `capabilities.ts` + los targets en el `SYSTEM_PROMPT` + evals ×3). **Carril de Borja.** Con ella, C12/C13/C14+B9 del eje `query` pasan de rojo a verde.
- **#693** — la decisión del modo mixto de P3 → [[structured-outputs-strict-garantiza-forma-no-veracidad]]
- **Fase 2** depende de #693 · **Fase 3** de #602 (`ready-for-human`) · **Anexo A** de la política RGPD.

⚠️ **Lo más valioso sin hacer, y no lo puedo hacer yo: la corrida real del eje `query`.** Está en `main` desde #680 y nadie la ha ejecutado — la maquinaria de medición existe y sigue sin usarse. Con creds: `npm run evals -- --only=query-coverage` → los 9 casos deben salir **ROJOS** y el eje aparecer en el scorecard, **no** en `"otros"`. Ese número es lo que convierte «esto mejora la cobertura» en un hecho.

_Dos correcciones al plan que salieron de implementarlo, y que no se reconstruyen leyendo el código:_ **tools y `SYSTEM_PROMPT` no son PRs independientes** → [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · y **P3 no es fontanería** sino una decisión de arquitectura, porque el modo strict prohíbe objetos libres.

_Entorno: el gate corre sin Docker con Homebrew (5432/6379) — arrancarlos o los `.pg` se autosaltan (212 skips vs 203) y el backstop no se prueba. **Dos gates seguidos contra el mismo Postgres cuelgan uno** (visto dos veces, una a 10 min); re-corrido solo, 35 s._ → [[tests-pg-self-skip-levantar-pgvector-local]]

## Bloqueantes

- **#482-p1 / #485** — esperando respuesta de Dani (email de Entra) y Borja (señal de prompt + contrato del audit); ver arriba.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).
- **#197/#228** (agendar futuro→calendario) — scope Entra `Calendars.ReadWrite` + admin consent (Borja).
- **SSH al host de prod** con timeouts intermitentes (visto en el drill) → diagnóstico vía panel/API Dokploy mientras.
- Secrets de prod → migrar a 1Password (pendiente recurrente).

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

- **21/22-jul — la base que sostiene todo lo de después** (cerrado, detalle en `docs/status-log/` y en el PROJECT-STATUS del repo): épica conversacional #118 (L1/L2a/L2b + anáfora a persona, recall ~100%) · **secretaria #467 completa** (reads fraseados grounded, small-talk, preferencias) · dedup de clientes #245 con `crm.mergeClients` · drill de voz #192 (6 hallazgos) · `ClientIntake` #451 como módulo único de alta · el agente como **2º escritor de `audit_log`** (#485) · self-recipient #482-p1 · módulo temporal único #452 · **épica de arquitectura #457**: gate raíz `npm run gate`, split actor/owner, `createApp` por slices en `src/composition/` (wiring: read/write → `capabilities.ts`, store → `persistence.ts`, env → `config.ts`, worker → `lifecycle.ts`) · Langfuse v3 con rutina de auditoría semanal · #532 (`meeting.update` con `participants` aditivo). Queda de ahí el tramo final de **#454** (switch de `routeTurn`, lane de Borja) y el **smoke conductual del self-recipient** → [[agh-qa-voz-guion-llamada]].

- **30-jul (mediodía, ya en prod)** — **Fase 0 (#531)**: eje `query` con 9 casos que nacen rojos a propósito + señal `no_target_miss`, y el guard RGPD del `reason` (era `string` libre reenviado verbatim a la traza). **P1 (#681)**: el scoping por (tenant, owner) pasa a ser error de compilación, y `ReminderStore.list` —el seam de la Fase 1— no tenía ni un test contra Postgres. → [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]]
- **30-jul (madrugada, ya en prod)** — **#672**: «Crea los 5» retoma el lote muerto. Dos hallazgos reordenaron el issue: la opción A del propio issue **no podía funcionar** (la ventana la borra el turno `write` que propuso el lote, y el ring exige id real con cap 4 < 5 → A necesitaba el mismo substrato durable, o sea que B era su paso 1), y **un puntero único pasaba el golden y fallaba la conversación real** → lista de 3 lotes muertos con desambiguación por cardinal y familia. La revisión adversarial (3 agentes, 8 hallazgos) encontró el peor: **el copy de error del propio sistema invitaba al secuestro** («Inténtalo de nuevo…», «lo reintentamos») → el usuario repetía lo que el agente le sugería y se le proponían cinco altas que nadie pidió. **#674**: «bórrala» sobre una nota **nunca funcionó en prod** (whitelist de runtime con 5 de 6 variantes; el e2e verde porque corre in-memory) — el candado vale más que el fix. → [[el-test-que-prueba-el-bug-es-la-traza-real-no-el-golden-del-issue]] · [[hitl-turnos-criticos-deterministas-antes-del-llm]] · [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]]
- **29-jul** — la primera comercial nueva (Itziar) rompió el agente en 45 min y salieron 9 issues; cerré 9 PRs en el día: #636/#638 (drift-gate y el calendario mudo), #640 (el dedup del alta miraba la cartera del owner y el índice único es de TENANT), #645, #644, #647 («sigue con lo nuevo», la frase que el propio copy ofrecía, confirmaba el lote viejo), #650, **#643** (🔴 el turno que borra un cliente se envenenaba a sí mismo → 14 min de usuaria atrapada) y #585. **El hallazgo que más vale (auditoría #668): los ejes `composition`/`confusion` estaban al 100% con la sesión rota — el agente no falla razonando, falla al ejecutar, corregir y recuperar.** → [[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]]
- **28-jul** — `email.send` roto en prod (**#624, causa raíz aún abierta**: buzón/licencia M365) + revisión cross-PR con Postgres real: 3 hallazgos serios en el lote de Borja, arreglados antes de mergear. Deuda de skips pagada (184/184 pg-tests). → [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **27-jul** — una llamada de voz real dio 13 fallos y 25 PRs; la conversación medida subió 35/43 → 40/45. → [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]


## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agh-qa-voz-guion-llamada]] (guion de QA en llamada real) · [[agentesia]] · [[top-of-mind]]

_Método de esta semana:_ [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
