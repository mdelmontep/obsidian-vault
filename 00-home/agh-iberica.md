---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-19
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

## Estado (2026-08-19, tarde) — **las CINCO del día mergeadas** · abiertas solo #1302 y #1360, de Borja

> ⚠️ Este bloque **no nombra el SHA de `main` a propósito**: un snapshot que nombra su punta no puede acertar (se desfasa con su propio merge). Se consulta con `git rev-parse --short origin/main`.

✅ **Las cinco PRs del 19-ago DENTRO** (`#1399 → #1400 → #1397 → #1398 → #1404`; **#941**, **#1363** y **#1358** cerrados, comprobado por `state`). Override de founder de Manu avisado en Slack antes de tocar `main`, de una en una y sin `--delete-branch`. La combinación se midió **antes** y la suma cuadró exacta sin residuo (`4340 + 17 + 12 + 6 = 4375`).

🎯 **Cerrado el track de fidelidad de resolución** — la clase de fallo que **no falla: acierta otra pregunta**, y por eso el comercial no la detecta (#1363 escribía sobre la reunión pasada; #1358, un `WHERE` que no casa devuelve **cero**, no error). 🔒 Tres candados del repo pusieron en rojo mi propio diff y **los tres tenían razón**; cero tests ajenos tocados. Detalle → [[agh-iberica-historico]] · [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]] · [[tests-que-caen-por-contencion-de-cpu-verificalos-aislados-antes-de-diagnosticar]] · [[importar-de-un-fichero-de-test-re-ejecuta-sus-casos]].

🟡 **Sigue siendo de Borja: la disyuntiva de #941** — reanudación **automática** (lo implementado, con motivo escrito) vs bajo petición. Es una línea y un caso.

🔴 **De las premisas falsas del 19-ago sigue vivo lo accionable:** **#1100 está abaratado** (`lastQuestion` SÍ cruza al intérprete, como `pendingQuestion` — no hay que construir proyección) y la causa raíz de **#938** es falsa: fallan **dos entradas en dos listas** de `proposal-retake.ts`, no el `cancel`. Detalle → [[agh-iberica-historico]].

🆕 **Issues nuevas del 19-ago (las tres `ready-for-agent`):** **#1401** (un `SIN VÍCTIMA` falso con el control COHERENTE — el barrido no seleccionó ninguna suite del consumidor; #1396 no lo caza) · **#1402** (importar de un `.test.ts` re-ejecuta sus casos) · **#1403** (el mapa de #1358 solo tiene un consumidor: `tasks` y `reminders` siguen con el literal).

⛔ **El instrumento de evals NO es cola de agente** (premisa caducada que se hereda): #738 y #1304 llevan `CLOSED`; lo vivo (#1026, #1361, #1009, #1002, #985) es `ready-for-human`.

🔴 **La cola sigue siendo el problema, no la velocidad:** 82 % de los `ready-for-human` sin dueño (#1351) y **8 fallos de llamadas reales** abiertos desde el 20-jul (#937 #938 #648 #649 #741 #912 #535 — **#941 ya cerrado**).

⏸️ **Lote parado, DECIDIDO que merece la pena pero NO hoy:** `~/wt-1064` (#1064+#1212+#1044A). Al retomarlo: **rebasar → congelar el prompt y volcar las descripciones renderizadas ANTES de pagar la corrida**.

📚 **Estados anteriores** → [[agh-iberica-historico]].

_Creds:_ `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ espacio final) · SSH del host en `ssh AGH` (el ítem «186» es del PANEL, no de SSH). **`opsa`, nunca `op`**; `item get` exige `--vault`.
## Bloqueantes

_(El backlog de issues vivos está más abajo, en «Backlog de issues»: es una consulta, no estado.)_

- 🔴🔴 **RGPD, y va PRIMERO — #1349 CONTESTADO el 18-ago y la respuesta es NO a las dos: el DPA no está firmado y el ZDR no está activo ni solicitado.** Ya no es «verificar», es **hacer**: dos acciones de panel de **MANU** en la organización `agentesia-lab` (`org-iE0lJRHrjWaSI4ugYc6P50Ze`, se declara *personal org*, pay-as-you-go). ⚠️ Son **tres cosas distintas**: «no entrenar» es el defecto y sí está; el **DPA** se firma; el **ZDR** se solicita y **se aprueba o no** (por defecto retienen ~30 días). El documento que ve el compliance de AGH ya **no las da por hechas** (#1383). Y sigue pendiente decidir si el piloto salta al escalón 2 (Azure tenant-UE), que por diseño del gateway es un flip de configuración. → [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]]
- 🔴 **De Manu, 2 minutos: las claves de API de Langfuse a 1Password → #1009** (OPEN y sin dueño; la tabla de #1351 las colgaba de #1284, que va de otra cosa). Sin ellas nadie puede correr la sonda desde un portátil.
- 🔴 **El disparador diario de la sonda sigue sin existir → #1361** (re-filiado: su único dueño era #1304, que está `CLOSED`, y su decisión se escribió 27 min DESPUÉS del cierre). Seguimos sin saber si Carlos usa la demo.
- 🔴 **HUMANO, en el panel de Dokploy:** activar el digest en lista con `WHATSAPP_OPEN_THREADS_LIST_PREFIX=hilos_semana` y `WHATSAPP_OPEN_THREADS_LIST_MAX=6`.
- 🔴 **DE MANU:** qué hacer con `d.martins`, que recibió tres mensajes con los hilos de otra persona. No se ha avisado a nadie.
- 🟠 **De Borja, una línea cada uno:** **#1032** (¿retirar `addCandidate` o construir su lectura? la medición respalda retirar) y **#1384** (`ready-for-human`: los **siete** comportamientos de Graph que #580 asume y **nadie ha medido** — no se midieron a propósito, un PATCH real manda correos a contactos de clientes y el camino seguro pide consentimiento OAuth en navegador).
- 🟠 **#1394** — los dos worktrees abandonados **ya no existen** (medido 19-ago, sin saber quién los quitó). Lo vivo es su **preflight** que avisa de worktrees retirables, con el candado que discrimine el que tiene trabajo dentro.

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

### Backlog de issues (consulta, no estado — `gh issue list --label ready-for-agent`)

- **Vivas, ya sin PR asociada** (las de la tanda del 7-ago están mergeadas). De la auditoría del 7-ago: **#1031** (el patrón: dashboard client-scoped) · **#1033** (pantalla «Lo mío», espera a #1000) · **#1030** (cancelar hablando; la anáfora en #1038, falta la referencia por cuerpo — cuesta evals) · **#1032** (`addCandidate`: se escribe, nadie lo lee, no se puede quitar) · **#1026** (`llm-smoke` no corre desde que existe) · #1019 · #1020 · #1036 · #1037. **Del 10-ago:** **#1095** (responder al digest no tiene NI UNA eval, y su disparador es un prefijo de texto que nadie asevera) · ~~#1086~~ (CERRADO 14-ago: eran **40 líneas en 15 ficheros** y **tres** importes) · **#1083** (`mutate:diff` no mide lo multilínea — 3 casos en un día) · **#1044** opción A · **#1072**.
- **Decisiones de Borja:** #738 (tolerancia del baseline — **el 22 % del banco no tiene NINGÚN suelo**) · #846 · #847 · #863 · #884 (la confirmación de borrado miente: `tasks … ON DELETE SET NULL`) · **#627** A/B (rec. **B**) · **#929** (`message.text`, toca prompt).
- **Sin dueño y fuera de la cola de arriba:** **#741** (ASR "Grabados"/"Dragados", golden escrito) · **#898** (dos colas de turno por (tenant,usuario), cae en #454).
- **Rastro de #817/#853:** **#818** (`client.prep` con el agujero que #733 cerró en `client.detail`) · **#820** · **#841** (la ventana que falta degrada en silencio estadístico).
- ⚠️ **`lastClientId` no caduca NUNCA** y se proyecta como entidad activa cada turno, mientras las oportunidades del mismo array sí pasan el TTL de 30 min → 2ª causa raíz del paso 5 de **#535**, que su caso-oro nº2 no cubre.
- **#870** — rojo crónico, task.create mete el contexto del mensaje en el título, 0/25 en `main`.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).


🧰 **Herramientas:** `~/.claude/bin/mutate` (4 modos que no miden nada; aborta si el control trajo recuento y el mutante no) y `npm run mutate:diff` en el repo, que **desde el 14-ago cubre `dashboard/`**. → [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]

**Acceso / infra (referencia):** **SSH al host** responde por el **5251** (password del ítem 1Password `ssh AGH` vía `SSH_ASKPASS`; el 22 sigue muerto) → ya usado para las auditorías #747/#668 de esta sesión. Detalle en **#760**. · Secrets de prod → migrar a 1Password (pendiente recurrente).

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

- **Hasta el 14-ago (Manu + Borja; ~100 PRs)** — el detalle por tramos, en [[agh-iberica-historico]]. Lo que sigue valiendo: **el gate verde no es la revisión**, la Fase 3 cerrada, el bypass del HITL (#945) y el arnés de medición (golden de copia, `mutate:diff`, evidencia de evals por huella).
- **21 jul – 3 ago — la base sobre la que corre todo lo de ahora** (cerrado; el día a día vive en `docs/status-log/` del repo). En orden: épica conversacional y drill de voz → la primera comercial nueva rompió el agente en 45 min y salieron 9 issues en un día → el plan de precisión entero en prod (Fases 0-3, eje `query` 72,7 % → 81,8 %) → el rediseño del dashboard (épica #767, cortes 01-04). 👉 **Lo que se lleva ese tramo, y sigue vigente:** cada fix medido contra el modelo real destapa el siguiente hueco, un guard nuevo se mide contra los datos que YA existen, y el gate verde no sustituye una revisión adversarial. Learnings: [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[el-test-que-prueba-el-bug-es-la-traza-real-no-el-golden-del-issue]] · [[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[hitl-turnos-criticos-deterministas-antes-del-llm]] · [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] · [[nul-byte-literal-en-markdown-hace-que-git-trate-el-archivo-como-binario]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]] · [[test-que-reaplica-una-migracion-congelada-estrecha-el-schema]] · [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]]



## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agh-qa-voz-guion-llamada]] (guion de QA en llamada real) · [[agentesia]] · [[top-of-mind]]

_Método de esta semana:_ [[el-borrado-de-rama-nunca-va-encadenado-al-merge]] · [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]] · [[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]] · [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]] · [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
