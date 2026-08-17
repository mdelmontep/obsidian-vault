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

## Estado (2026-08-17) — `main` en `5d3c473`; **TABLERO VACÍO**: cero PRs abiertas de nadie

🟢 **Dentro el 17-ago (madrugada): 6 PRs y 6 issues** (`8863b57` → **`5d3c473`**) — #1274/#1272 · #1275/#1265 · #1276/#1269 · #1277/#1259 · #1278/#1258 · #1279/**#1256** (la única que toca `src/` del agente) · #1283/cierre. Seis agentes en paralelo, superficies disjuntas contadas fichero a fichero, **coste de evals CERO** (medido con `containsPromptMarker` real: `hitl-brain.ts` **no** es fuente de prompt aunque #1256 lo parezca). Prod verificada por contenido (`sha256:af532053…`, 304 ficheros, construida ~1 min después de `feece17`).

🔑 **Lo reutilizable del 17-ago:**
- **El hueco está en la PROPIEDAD que la PR declara como su aportación** — dos de dos SIN VÍCTIMA al revisar trabajo ajeno. Y **`0 SIN VÍCTIMA` del barrido no cubre nada mientras «sin medir» no sea 0**: revertir el hunk entero no compila y cae en esa categoría; borrar solo la llamada sí mide. → [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]]
- **La combinación se compila ANTES de mergear, y los contadores tienen que CUADRAR**: `3534 = 3489+4+14+19+8` y `1271 = 1257+14` — sumar las PRs por separado da el mismo número que juntarlas, o sea que nada se pisa ni desaparece.
- **`git cherry` no vale tras un squash de varias ramas** (dio 2, 5 y 7 «sin mergear» estando las seis dentro): decide comparar **los ficheros de cada rama** contra `main`. Y el flake `57P01` es de **CARGA, no de diff** — 4 de 6 corridas lo tuvieron a load 31-38, la combinación en calma salió limpia.

🧾 **Issues nuevos (4):** **#1280** (el `decline` del `execute` sigue crudo por voz: `failure.userReply` no pasa por el seam — radio = **todo** `UserFacingError`) · **#1281** `ready-for-human` (**`agh-postgres` no pertenece a ningún proyecto compose**, `Labels` = `{}`: `DRIFT_MODE=docker` es inejecutable contra el 5433 — tercera vez que ese camino cuesta tiempo) · **#1282** (el marcador del aviso de deriva es un literal: el candado ve que el emisor CAMBIE, no que aparezca uno NUEVO, **y #1268 lo estrena**) · **#1273** (botón de Entra sin gatear).

---

📚 **Estados anteriores** → [[agh-iberica-historico]]. **16-ago (tarde)**: 8 PRs y 10 issues (`c24d5c9`→`8863b57`) — su lección (`MERGEABLE` no es «el diff es el tuyo») **ya está en la regla 6 de `CLAUDE.md` desde #1272**. **15-ago (noche)**: 13 PRs y 14 issues.

⏸️ **Lo único vivo a propósito:** rama `manu/issue-1064-1212-1044-campo-aislado-y-huella` (#1064 + #1212 + #1044A) en `~/wt-1064`, **sin PR**. #1212 y #1044A hechos — y #1212 trae la cifra que faltaba: de los alias de FILTRO difieren **0** entre `toLowerCase` y `foldKey`, pero **de los 13 de ORDEN difieren 2**. Falta el caso-oro de #1064 y el prompt **cambió de verdad**, así que abrirla sería declarar cobertura de eval CERO sobre un cambio real de prompt (~12 $ para medir una PR sin su propia eval).

▶️ **#1204 desbloqueado** al entrar #1246 (era UN fichero, y no se puede partir: `noUnusedLocals` exige arreglar los **18 símbolos** a la vez). ⚠️ Sus tres `_Aridad*` de `tone.ts` son el candado de tipos de #1154: **borrarlos apaga la verificación** y **exportarlos** dispara `exports-fantasma` (`2 failed | 31 passed`); queda `satisfies`. La familia `tone` (#1144 · #1146 · #1161 · #1052) no es paralelizable: comparten `test/golden/copy-por-canal.txt`.

---

🗓️ **14 y 15-ago, condensado** (detalle → [[agh-iberica-historico]]): 11 PRs y 12 issues la mañana del 15 · 17 issues el 14 en dos tandas · 11 de 16 premisas falsas en cuatro días · las 4 decisiones de producto de esa mañana, **tres implementadas** · #1097→#1098 mergeadas, que es lo que desbloqueó #1144·#1146·#1161 (ya dentro hoy).
✅ **Prod se verifica por CONTENIDO y sin SSH**: `curl …/version` vs `build:stamp --print` en árbol limpio → [[sellar-la-imagen-en-el-build-para-saber-que-corre-en-prod-sin-shell]]. El SSH del host **NO está caído** (`nc 5251` succeeded, medido dos veces).

📋 **Cola libre**: los 4 nuevos de arriba + los del 16-ago que quedan (#1257 · #1260 · #1261 · #1262) + **#1268** (deuda de #1248, **DESBLOQUEADO**: su fichero ya está en `main`) + **#1188** (barrido de fixtures no discriminantes; esta tanda aporta **4 casos nuevos** de esa familia, ya cerrados dentro de #1269 — o sea que el patrón no era de aquel fichero). ⚠️ **#1268 y #1282 hay que ordenarlos entre sí**, no dejarlo al azar de quién coja cuál. **Decisiones mías SIN tomar:** #1167 · #1129 · **#1281** (recrear `agh-postgres` desde el compose, o declarar el modo docker como solo-CI). **#1180 ya decidida (NO entra), no re-litigar**.

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
