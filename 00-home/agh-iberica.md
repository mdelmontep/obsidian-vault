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

## Estado (2026-07-30, madrugada) — 3 PRs esperando merge, y dos bugs que los tests no podían ver

**`main` sigue en `2c29eff`** — esta sesión no mergeó nada. Abiertas y verdes: **#676** (#672), **#677** (#674) y **#678** (solo-docs, el cierre). #676 reclama la **migración 0024**; las dos primeras tocan los mismos dos ficheros en regiones distintas, así que **la segunda hay que rebasarla** (sugerido: #676 antes, es el bug que reporta Carlos).

**#672 — «Crea los 5» retoma el lote que murió.** Dos hallazgos que reordenaron el issue: (a) **la opción A que proponía no podía funcionar** — la ventana de turnos la borra el propio turno `write` que propuso el lote, el ring exige id de fila REAL y su cap es 4 < 5, o sea que A necesitaba el MISMO substrato durable y B era su paso 1; (b) **un puntero único pasaba el golden del issue y fallaba la conversación real** (la nota intermedia de #649 lo sobrescribía) → lista de 3 lotes muertos con desambiguación por cardinal y por familia de entidad. → [[el-test-que-prueba-el-bug-es-la-traza-real-no-el-golden-del-issue]]

:rotating_light: **Lo que encontró la revisión adversarial (3 agentes, 8 hallazgos, arreglados antes de abrir la PR):** el peor es que **el copy de error del propio sistema invitaba al secuestro** — «Inténtalo de nuevo en un momento» (y «lo reintentamos» del marcador M365, el fallo más frecuente en prod) eran frases que mi matcher se quedaba, así que tras un read roto el usuario repetía lo que el agente le sugería y se le proponían cinco altas que nadie pidió. Forma exacta de #647 y **peor que el bug que cerraba**. → [[hitl-turnos-criticos-deterministas-antes-del-llm]]

**#674 — «bórrala» sobre una NOTA nunca funcionó en prod.** La whitelist de runtime de `parseLastWrite` listaba 5 de las 6 variantes del tipo: el puntero se escribía bien en JSONB y se leía `undefined`. El e2e estaba verde porque corre in-memory. El candado (derivar la lista de un `Record`, que no compila si falta un miembro) vale más que el fix, y **el patrón correcto ya existía dos funciones más allá**. → [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]] · [[fake-vs-postgres-orden-sort-utf16-vs-collation]]

**A humano (Borja):** **#675** (RGPD — la purga en disco de los lotes retomables caducados; no cablé el worker a propósito porque toca `src/composition/`, imán de conflicto, justo al arrancar el schema de staffing) · **la opción A de #672** (lista dictada a la proyección del intérprete + evals ×3: con el substrato puesto es una línea en `llm-turn-interpreter.ts:324`, y es lo único que cubre paráfrasis abierta y composición sobre la referencia) · lo de antes sigue vivo: **#624 espera un correo dictado**, #648/#649/#651 y los forks de #580/#627/#585 son su carril, **#579 de Dani lleva tres días lista sin mergear**, `RETELL_WS_SECRET` sin definir en prod.

_Entorno: el gate corre entero sin Docker con los servicios de Homebrew (5432/6379); el drift-gate exige `pg_dump` de la misma major que el servidor →_ [[tests-pg-self-skip-levantar-pgvector-local]]

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

- **21/22-jul — la base que sostiene todo lo de después** (cerrado, detalle en `docs/status-log/` y en el PROJECT-STATUS del repo): épica conversacional #118 (L1/L2a/L2b + anáfora a persona, recall ~100%) · **secretaria #467 completa** (reads fraseados grounded, small-talk, preferencias) · dedup de clientes #245 con `crm.mergeClients` · drill de voz #192 (6 hallazgos) · `ClientIntake` #451 como módulo único de alta · el agente como **2º escritor de `audit_log`** (#485) · self-recipient #482-p1 · módulo temporal único #452 · **épica de arquitectura #457**: gate raíz `npm run gate`, split actor/owner, `createApp` por slices en `src/composition/` (wiring: read/write → `capabilities.ts`, store → `persistence.ts`, env → `config.ts`, worker → `lifecycle.ts`) · Langfuse v3 con rutina de auditoría semanal · #532 (`meeting.update` con `participants` aditivo). Queda de ahí el tramo final de **#454** (switch de `routeTurn`, lane de Borja) y el **smoke conductual del self-recipient** → [[agh-qa-voz-guion-llamada]].

- **29-jul** — la primera comercial nueva (Itziar) rompió el agente en 45 min y salieron 9 issues; cerré 9 PRs en el día: #636/#638 (drift-gate y el calendario mudo), #640 (el dedup del alta miraba la cartera del owner y el índice único es de TENANT), #645, #644, #647 («sigue con lo nuevo», la frase que el propio copy ofrecía, confirmaba el lote viejo), #650, **#643** (🔴 el turno que borra un cliente se envenenaba a sí mismo → 14 min de usuaria atrapada) y #585. **El hallazgo que más vale (auditoría #668): los ejes `composition`/`confusion` estaban al 100% con la sesión rota — el agente no falla razonando, falla al ejecutar, corregir y recuperar.** → [[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]]
- **28-jul** — `email.send` roto en prod (#624, causa raíz aún abierta: buzón/licencia M365) + revisión cross-PR con Postgres real: 3 hallazgos serios en el lote de Borja, arreglados por él antes de mergear. Deuda de skips pagada: 184/184 pg-tests. → [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]]
- **27-jul** — de una llamada de voz real salieron 13 fallos y 25 PRs; conversación medida 35/43 → 40/45. Lección: medir contra el modelo real DESPUÉS de mergear destapa el siguiente hueco. → [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]


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

[[agh-qa-voz-guion-llamada]] (guion de QA en llamada real) · [[agentesia]] · [[top-of-mind]]
