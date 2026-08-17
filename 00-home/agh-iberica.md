---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-17
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

## Estado (2026-08-17, noche) — `main` en `7c9bd36`; abierta solo la #1302 de Borja

🟢 **DOCE PRs dentro y DOCE issues cerrados** (#1309 · #1204 · #1291 · #1188 · #1308 · #1305 · #1306 · #1289 · #1262 · #1052 · #1300 · #1304; último código `94b99a3`). Gate sobre `main` **✓ verde a la primera y sin reintento** (`3748/239/5f · dashboard 1273/0/0f`), prod verificada por contenido (`sha256:d9b20f01… · 309 ficheros`), y la **combinación de las doce medida ANTES de mergear** con la suma exacta (3748).

🔴 **Lo más valioso: #1291 pedía un candado que NO puede existir**, y lo demostró el gate — la invariante que el issue pedía era el **diagnóstico** de `mutate-diff.ts`. → [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]]. De paso, el defecto real es peor de lo escrito: el parser mentía en las **cuatro** cifras y en **toda** corrida con fallos.

🔴 **La verificación de la combinación COBRÓ** (acoplamiento del 15-ago calcado): el `lint` de las doce juntas salió rojo por una constante sin usar que **sólo existe al juntar #1315 con #1317** — ninguna PR podía verlo sola. Y la constante no sobraba: **faltaba el caso que la consumiera** (el corpus aseveraba que el embudo grita, no que rinda).

🐛 **Defecto de PRODUCCIÓN vivo → #1322**: `spokenLine("b@617314938.com")` **destapa** el teléfono, porque la pasada de correo quita la `@` que lo protegía; el TTS lo dirá como cantidad (#977 otra vez). Lo probado era `spokenPhones` **a solas** — nadie había mirado la composición. Cae con él la afirmación del código de que el orden de las pasadas es una «mutación equivalente». **Es el siguiente a coger.**

📡 **#1304: no había ninguna sonda que arreglar** — cero líneas del repo vigilaban Langfuse; lo que llamábamos sonda era el `curl` a `/health` de la auditoría semanal. La nueva mide el **almacén**. ⚠️ **Pero nada la ejecuta todavía**: sin disparador diario es otra señal que nadie lee. Decidir dónde vive el job.

⚠️ **Tres premisas de issues resultaron falsas, dos MÍAS**: #1309 (los `created_at` **no** empatan: están separados 8-11 ms, y su arreglo propuesto tampoco valía → [[order-by-created-at-empata-dentro-de-la-misma-transaccion]], corregido) · #1305 (cinco puntos de emisión, no cuatro) · #1052 (la asimetría de tonos que daba por heredada no existe).

▶️ **Cola libre, priorizada**: **#1322** (el único de producción) · **#1323** (`copyForChannel` escrita dos veces) · **#1327** · **#1326** · **#1325** · **#1095** · **#992** · **#991** · **#984**. `ready-for-human`: **#1324** · **#1288** · **#1307**.

⚠️ **Aviso para la #1302 de Borja**: #1204 metió `@typescript-eslint/no-unused-vars` en la raíz y el barrido de lint ve los ficheros nuevos de los DOS paquetes — si alguno de los suyos trae un símbolo sin usar, saldrá en su corrida.

⏸️ **Lo único vivo a propósito:** rama `manu/issue-1064-1212-1044-campo-aislado-y-huella` en `~/wt-1064`, **sin PR** — falta el caso-oro de #1064 y el prompt cambió, así que abrirla declararía cobertura de eval CERO sobre un cambio real (~12 $). ⚠️ **Y sigue sin saberse si Carlos usa la demo**: 1.064 trazas en cinco semanas, con días de 4 y 6 — «sin trazas» y «sin tráfico» son indistinguibles.

📚 **Estados anteriores** → [[agh-iberica-historico]] (**17-ago tarde, mediodía y madrugada** condensados ahí).

_Creds:_ `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ espacio final) · SSH del host en `ssh AGH` (el ítem «186» es del PANEL, no de SSH). **`opsa`, nunca `op`**; `item get` exige `--vault`.

## Bloqueantes

- 🔴 **HUMANO, en el panel de Dokploy:** activar el digest en lista con `WHATSAPP_OPEN_THREADS_LIST_PREFIX=hilos_semana` y `WHATSAPP_OPEN_THREADS_LIST_MAX=6`. ⚠️ **El tope es el tramo CONTIGUO aprobado desde 1, no cuántas plantillas hay creadas**: `hilos_semana_7` seguía en revisión y con `MAX=8` un digest de 7 hilos falla el envío entero. Sin las dos envs, #1094 no cambia nada en prod (deliberado).
- 🔴 **DE MANU:** qué hacer con `d.martins`, que recibió tres mensajes con sus hilos. No se ha avisado a nadie.
- ✅ *Cerrados y sin cola: #952 (el digest entregó, 10-ago) · #988 (el teléfono se lee dígito a dígito) · #953 (los 3 hilos pasaron a `delivered`) · **#1094 y #1096 MERGEADAS** (el hub las listó como bloqueante de Borja hasta el 14-ago, ya siendo falso).*
- ✅ *RESUELTO (14-ago): prod se verifica por contenido con `curl …/version` vs `build:stamp --print` en árbol limpio. ⚠️ La app es `agente.agh.agentesialabs.com`; `agh.agentesialabs.com` es el PANEL, y su 200 no prueba nada (#780).*
- **Vivas, ya sin PR asociada** (las de la tanda del 7-ago están mergeadas). De la auditoría del 7-ago: **#1031** (el patrón: dashboard client-scoped) · **#1033** (pantalla «Lo mío», espera a #1000) · **#1030** (cancelar hablando; la anáfora en #1038, falta la referencia por cuerpo — cuesta evals) · **#1032** (`addCandidate`: se escribe, nadie lo lee, no se puede quitar) · **#1026** (`llm-smoke` no corre desde que existe) · #1019 · #1020 · #1036 · #1037. **Del 10-ago:** **#1095** (responder al digest no tiene NI UNA eval, y su disparador es un prefijo de texto que nadie asevera) · ~~#1086~~ (CERRADO 14-ago: eran **40 líneas en 15 ficheros** y **tres** importes) · **#1083** (`mutate:diff` no mide lo multilínea — 3 casos en un día) · **#1044** opción A · **#1072**.
- **Decisiones de Borja:** #738 (tolerancia del baseline — **el 22 % del banco no tiene NINGÚN suelo**) · #846 · #847 · #863 · #884 (la confirmación de borrado miente: `tasks … ON DELETE SET NULL`) · **#627** A/B (rec. **B**) · **#929** (`message.text`, toca prompt).
- **Sin dueño y fuera de la cola de arriba:** **#741** (ASR "Grabados"/"Dragados", golden escrito) · **#898** (dos colas de turno por (tenant,usuario), cae en #454).
- ⚠️ **`lastClientId` no caduca NUNCA** y se proyecta como entidad activa cada turno, mientras las oportunidades del mismo array sí pasan el TTL de 30 min → 2ª causa raíz del paso 5 de **#535**, que su caso-oro nº2 no cubre.
- **Rastro de #817/#853:** **#818** (`client.prep` con el agujero que #733 cerró en `client.detail`) · **#820** · **#841** (la ventana que falta degrada en silencio estadístico).
- **#870** — rojo crónico, task.create mete el contexto del mensaje en el título, 0/25 en `main`.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

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

_Método de esta semana:_ [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
