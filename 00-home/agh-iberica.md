---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-30
tags: [cliente, agh-iberica, agente-comercial, mastra, m365, whatsapp, multi-tenant, HUB]
---

# AGH Ibérica — Paquita, la agente comercial

HUB del proyecto. Empresa de IT que da servicio a grandes multinacionales (Dragados, McDonald's, aseguradoras). Quieren que **AIA agentesIA sea su departamento de IA**. Modelo: AGH = prime contractor / canal comercial; **AIA = brazo de delivery**. Todo lo construido debe ser **empaquetable y reutilizable** para que AGH lo revenda.

**Contacto:** Carlos (CEO de AGH Ibérica España).

## Producto en curso: **Paquita**, agente comercial

> ⚠️ **El agente se llama Paquita. «Carlos» es el CEO de AGH**, nunca el nombre del agente. El error nació en este hub, contaminó a un tercero y se corrigió en el repo por #1422 (26-ago).

Agente conversacional **interno** (secretario/CRM) para los propios comerciales de AGH. Primera versión/demo que testeará el propio Carlos (el CEO). Se habla por **WhatsApp (voz in / texto out)** y **llamada de voz (Retell)**.

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

## Estado (2026-08-26) — **Paquita ya emite al portal de Flota IA**, pero nadie ha podido comprobar que emita

> ⚠️ Este bloque **no nombra el SHA de `main` a propósito**: un snapshot que nombra su punta no puede acertar (se desfasa con su propio merge). Se consulta con `git rev-parse --short origin/main`.

✅ **#1418 en prod: el emisor `custom_api` hacia Flota IA.** Una interacción = un TURNO; agrupar por llamada sigue abierto en #1419. Detalle → [[agh-iberica-historico]].

🟡 **NADIE ha probado que emita, y el cero medido NO discrimina.** El portal midió a las 20:30 (cero filas, `last_error` NULL, cero `error`) pero `docker logs` da **cero webhooks entrantes**: Paquita no ha tenido ni un turno ⇒ «no emitió» y «no hubo nada que emitir» son la misma observación. Falta **un WhatsApp real** y repetir el SELECT anclando a la hora del `POST /webhook/whatsapp`, no al arranque. → [[una-ventana-de-observacion-anclada-al-arranque-caduca-con-cada-merge]]

🔴 **#1424** — el emisor **solo escribe log cuando FALLA**, así que «apagado» y «funcionando» son el mismo silencio en nuestros logs. Es la causa raíz de que hoy hiciéramos arqueología en dos bases de datos para no concluir nada. El portal descartó el latido contra su ingesta (ensuciaría `agent_interactions`, y `is_test` no salva la tabla que luego juzga la fase 2): a cambio, dos líneas nuestras, una por proceso.

📚 **Estado del 19-ago (fidelidad de resolución: #941/#1363/#1358)** → [[agh-iberica-historico]]. Vivo de ahí: la disyuntiva de #941 es de Borja (una línea) · #1100 abaratado · la causa raíz de #938 es falsa · #1401/#1402/#1403 `ready-for-agent`.

⛔ **El instrumento de evals NO es cola de agente** (premisa caducada que se hereda): #738 y #1304 llevan `CLOSED`; lo vivo (#1026, #1361, #1009, #1002, #985) es `ready-for-human`.

🔴 **La cola sigue siendo el problema, no la velocidad:** 82 % de los `ready-for-human` sin dueño (#1351) y **8 fallos de llamadas reales** abiertos desde el 20-jul (#937 #938 #648 #649 #741 #912 #535).

⏸️ **Lote parado, DECIDIDO que merece la pena pero NO hoy:** `~/wt-1064` (#1064+#1212+#1044A). Al retomarlo: **rebasar → congelar el prompt y volcar las descripciones renderizadas ANTES de pagar la corrida**.


_Creds:_ `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ espacio final) · SSH del host en `ssh AGH` (el ítem «186» es del PANEL, no de SSH). **`opsa`, nunca `op`**; `item get` exige `--vault`.
## Segundo frente (30-ago): la contabilidad de AGH sale de Yooz a TuFacturaIA

Independiente de Paquita y con otro interlocutor (Giuliana y Daniela llevan la contabilidad;
Carlos solo decide umbrales). Yooz es un **piloto aparcado**: 46 facturas, 39 sin codificar,
cero exportaciones nunca. El cuello de botella de AGH es codificar, no la herramienta.

**Descubrimiento cerrado, implementación sin arrancar** (decisión de Manu). Ya en mano y sin
depender de Mazars: el `.TRA` de Cegid V9 mapeado campo a campo y los catálogos del tenant
(235 cuentas de 11 dígitos, 40 proveedores, 4 IVAs, ejes `CANAL`/`DEPARTAMENTO`, circuito de
3 etapas). 👉 Falta preguntar a Carlos los **umbrales de aprobación por importe**.

⛔ Tenant en **solo lectura**; **no se solicita** a Yooz la exportación de reversibilidad
(integramos, no rescindimos). Housekeeping: borrar el export `TRA_PRUEBA`.

Detalle, plan verificado y aprendizajes → [[facturaia-yooz-agh-migracion]]

## Bloqueantes

_(El backlog de issues vivos está más abajo, en «Backlog de issues»: es una consulta, no estado.)_

- 🔴🔴 **Langfuse no guarda trazas desde el 23-ago 03:00 (#1284).** ClickHouse **no existe** en el host (`/api/public/traces` → 500 `EAI_AGAIN clickhouse`) y aun así `/api/public/health` da **200** (#1304). **Segunda vez**: cayó el 17-ago, se reparó, escribió del 19 al 23 y volvió a caer ⇒ **repara pero no cura**; causa desconocida (sin OOM, disco y RAM de sobra, nada en cron a las 03:00). ⚠️ **Nada de `docker volume prune`**: el volumen sobrevivió las dos veces (38 GB, del 5-jul, nunca recreado) y #1284 lo daba por perdido — falso. Receta: [[docker-infra]] §«Un servicio AUSENTE se levanta solo». 👉 Mientras siga así, **#1361 y #1009 miden un sitio que no guarda nada**.
- 🔴 **El DPA con AGH NO está firmado y la FIRMA no está en ninguna cola** (#1350 OPEN, de Borja, **sin fecha objetivo ni ubicación del documento**). Se opera igualmente por **decisión de Manu del 26-ago asumiendo el riesgo**: es decisión de negocio, **no cobertura documental**. → [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]]
- 🔴🔴 **RGPD OpenAI — #1349 contestado el 18-ago: el DPA no está firmado y el ZDR no está activo ni solicitado.** Ya no es «verificar», es **hacer**: dos acciones de panel de **MANU** en `agentesia-lab` (`org-iE0lJRHrjWaSI4ugYc6P50Ze`). ⚠️ Son **tres cosas distintas**: «no entrenar» es el defecto y sí está · el **DPA** se firma · el **ZDR** se solicita y **se aprueba o no** (por defecto retienen ~30 días). El doc que ve el compliance de AGH ya no las da por hechas (#1383). Pendiente aparte: si el piloto salta al escalón 2 (Azure tenant-UE), que es un flip de configuración.
- 🔴 **De Manu, 2 min: claves de API de Langfuse a 1Password → #1009** (OPEN, sin dueño). Sin ellas nadie corre la sonda desde un portátil — pero ver el bloqueante de arriba: hoy no hay nada que sondear.
- 🔴 **El disparador diario de la sonda sigue sin existir → #1361** (su único dueño era #1304, `CLOSED`). Seguimos sin saber si Carlos usa la demo.
- 🔴 **HUMANO, en el panel de Dokploy:** activar el digest en lista con `WHATSAPP_OPEN_THREADS_LIST_PREFIX=hilos_semana` y `WHATSAPP_OPEN_THREADS_LIST_MAX=6`.
- 🔴 **DE MANU, 10 segundos:** mandar **un WhatsApp a Paquita** — es lo único que falta para saber si el emisor de #1418 emite. Y crear el incoming webhook de `#alertas-flota` (`C0BT7SLJ4G0`) para pegarlo en `/agency/admin` → conector Slack (hoy el aviso de silencio entrega en `#02-consumo-clientes`). Ninguna sesión puede hacer ninguna de las dos.
- 🔴 **DE MANU:** qué hacer con `d.martins`, que recibió tres mensajes con los hilos de otra persona. No se ha avisado a nadie.
- 🟠 **De Borja, una línea cada uno:** **#1032** (¿retirar `addCandidate` o construir su lectura? la medición respalda retirar) y **#1384** (los **siete** comportamientos de Graph que #580 asume y **nadie ha medido** — a propósito: un PATCH real manda correos a clientes).
- 🟠 **#1394** — lo vivo es el **preflight** que avise de worktrees retirables, con un candado que discrimine el que tiene trabajo dentro (los dos abandonados ya no existen).

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

_Método de esta semana:_ [[una-ventana-de-observacion-anclada-al-arranque-caduca-con-cada-merge]] · [[rebuild-no-recrea-el-contenedor-y-el-sello-de-build-es-ciego-al-reinicio]] · [[el-borrado-de-rama-nunca-va-encadenado-al-merge]] · [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]] · [[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]] · [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]] · [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
