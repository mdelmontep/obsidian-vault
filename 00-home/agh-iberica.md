---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-15
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

## Estado (2026-08-15) — `main` en `ff1ce5d`; **13 issues cerrados**, CERO PRs mías, **4 decisiones tomadas**

🟢 **Dentro el 15-ago: 11 PRs y 12 issues**, en tres trenes con gate de la COMBINACIÓN detrás de cada uno más una cuarta entrega (`842a72a` → `fc9c134` → `4405c6e` → `4257d7d` → **`a8dc258`**, + cierre `ff1ce5d`). Último gate `agente 3355/239/5f · dashboard 1226/0/0f` ✓. **Prod verificada por contenido al cerrar**: `sha256:83022abf… · 302 ficheros`, idéntico en `/version` y en el árbol de `ff1ce5d`. Nota de sesión y snapshot **dentro de `main`**.

🔑 **Lo reutilizable del 15-ago:** *(a)* **6 de 7 premisas falsas y TODAS cortas** (65 ficheros → 77 de 797; una fecha con 12 días de error; 19 exports no vivos → 24). *(b)* **noveno hueco en el CABLEADO**: cablear el arreglo bueno **no protege** — volver al barrido naive dejaba las suites en verde; la clase se cierra en el **instrumento**, sobre lo versionado, no con un candado por consumidor. *(c)* **un candado que vive en `tsc` es invisible para la suite Y para el barrido de mutación** → [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]]. *(d)* **el escáner de estados TAMPOCO basta**: no conoce los literales de regex y puede dejar MUDO al guard de evals (#1221) → [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]. *(e)* **las convenciones se descartan con la cifra**: `Fake*`/`InMemory*` casaba los 11 dobles, pero **26 de los 37** símbolos que empiezan así están VIVOS..

🧾 **Issues nuevos del 15-ago (8 vivos):** #1204 · #1206 · #1211 · #1212 · #1215 · #1218 · #1219 · #1222 — todos con etiqueta comprobada. **#1221 y #1216 se abrieron y CERRARON el mismo día**: el guard de evals podía callarse (su escáner no conocía los literales de regex, y traía el gemelo que su propio test anunciaba sin cubrir), y la regla de #1182 ya está escrita en `~/.claude/rules/type-safety-ts.md` → [[un-candado-que-vive-en-tsc-es-invisible-para-la-suite-y-para-la-mutacion]].

✅ **Las CUATRO decisiones de producto, TOMADAS el 15-ago y escritas en su issue** (pendientes de implementar, cero coste de evals en las tres primeras — medido, ninguno de sus ficheros es fuente de prompt):
- **#1196 → NO**: `formal` tampoco lee su plantilla por voz; se retira `formalProposeVoice[2]`. ⚠️ cambiar el tamaño del pool hace a `pickVariant` (`hash % tamaño`) **rebarajar qué molde oye cada comercial** — el diff del golden es la evidencia.
- **#1116 → nombrar la etapa**: «Tienes 1 oportunidad **en negociación**». ⚠️ el candado debe aseverar que NOMBRA la etapa; un `toContain("1")` pasaría con el copy viejo.
- **#1103 → quitar `Mail.Send`** de los scopes, sin forzar reconexión. ⚠️ el candado bueno ata los scopes a lo que el código EJERCE, no a otra lista.
- **#1092 → adelante**, pero **el paso 1 es humano**: mandar `hilos_pendientes_3` a un móvil real y ver si llegan los saltos. Que Meta apruebe el cuerpo no prueba que WhatsApp lo entregue.

🟢 **Dentro el 14-ago (17 en el día):** #1190/#1183+#809 · #1187/#1178 · #1194/#1176 · #1198/#1173+#1174 · #1199/#1171 (la imagen deja de copiar `dashboard/`, −34,8 % de la capa) · #1202/#1179, más los once de mañana y tarde. Detalle en `docs/status-log/` del repo.

✅ **Prod se verifica por CONTENIDO y sin SSH**: `curl …/version` vs `npm run build:stamp -- --print` en árbol limpio → [[sellar-la-imagen-en-el-build-para-saber-que-corre-en-prod-sin-shell]]. **El SSH del host NO está caído** (`nc 5251` → succeeded, medido dos veces; sin probar autenticación) — la premisa «5251 timeout» se heredaba y era falsa.

🔑 **Del 14-ago, condensado** (detalle en `docs/status-log/`): 11 de 16 premisas falsas y el sesgo NO es constante — *la cifra que nadie midió está mal en la dirección que le convenga al relato*, y **la recomendación de un issue es la premisa que menos se cuestiona**. Más: el hueco en el cableado → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · mide cuántos pueden fallar antes de elegir N candados → [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]] · [[aseverar-la-igualdad-congela-un-accidente-asevera-el-bicondicional]] · [[un-fichero-nuevo-es-un-solo-hunk-y-el-barrido-de-mutacion-no-lo-cubre]] · [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]] · [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]].

🧰 **En cola para Borja:** **#1097 → #1098, apiladas** — ⚠️ al mergearlas, squashear el padre deja a la hija `CONFLICTING`, **o `MERGEABLE` reaplicando el diff del padre**: `gh pr edit --base` no arregla la historia, hace falta `git rebase --onto origin/main <rama-padre>` → [[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]]. Desbloquean **#1144 · #1146 · #1161** (las tres en `hitl-brain.ts`). Además **#1126** · **#1129**. ⚠️ **#1036/#1037 caen en `static.ts` con la #1140 de Dani: apilar, no paralelizar.**

📋 **Cola libre**: los 8 nuevos de arriba + **#1188** (barrido de fixtures no discriminantes) del lote del 14-ago. **Decisiones mías que siguen SIN tomar:** #1167 · #1129. **#1180 ya decidida (NO entra), no re-litigar**.

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

- **13/14-ago (Manu; 27 PRs en dos días)** — el 13 cinco y el 14 **veintidós**, todas de arnés y medición: golden de copia por canal, `verify:ui` que ABRE lo que hay que abrir, el coste de evals en un sitio, la línea `pg:`, el barrido cubriendo `dashboard/`, el **sello de imagen que verifica prod sin SSH**, el sello que dice la base real con pila, el candado del export fantasma, el punto ciego de las at-rules y la imagen sin `dashboard/` (−34,8 %). **Lo que sobrevive: 11 de 16 premisas falsas, y el sesgo NO es constante** — unas se quedan cortas, otras se pasan (una cifra mía, «cinco semanas», eran 8 días). Corolarios: *la lista objetiva sale del `git diff`, no de tu hipótesis*; *`Refs` y nunca `Closes` cuando entra media issue*; *el hueco está en el CABLEADO*, seis veces en la semana. → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[mide-cuantos-pueden-fallar-antes-de-elegir-entre-n-candados-y-un-tripwire]] · [[un-fichero-nuevo-es-un-solo-hunk-y-el-barrido-de-mutacion-no-lo-cubre]] · [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]] · [[dockerignore-no-es-gitignore-y-la-basura-local-pone-el-gate-rojo]] · [[aseverar-la-igualdad-congela-un-accidente-asevera-el-bicondicional]] · [[closes-N-cierra-el-issue-entero-aunque-escribas-3-de-4-al-lado]]
- **7/10-ago (Manu + Borja; 17 PRs)** — **el gate verde no es la revisión** (dos PRs devueltas con el gate verde; su candado pasaba con la regla borrada) · nace `npm run mutate:diff` (#1049/#1051) · `agh_dev` **envenenada** y el remedio escrito pasaba de «envenenada» a «desfasada» imprimiendo éxito · **41 de 41 runs de Actions con 0 pasos**, o sea 10 PRs mergeadas con un CI que no ejecutó nada. → [[registrar-una-migracion-sin-ejecutarla-envenena-la-bd]] · [[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]] · [[el-rojo-de-ci-tiene-dos-causas-cuenta-los-pasos-ejecutados]]
- **3→6-ago (Manu; ~50 PRs en cuatro días)** — Fase 3 en código y cerrada, cortes del rediseño, el bypass del HITL (#945), el sweeper (#953), las 7 issues de voz y dos trenes mergeados de una en una con gate entre cada uno. El hilo de los cuatro días: **un candado que EXISTE no es un candado que MUERDE**, y **cuatro instrumentos mintieron en la dirección que deja mergear** (`n=10` habría dejado pasar una caída de 96 % → 48 %). Método que rindió y se quedó: revisar las PRs propias con agentes instruidos para **atacar** las afirmaciones. → [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[evidencia-fechada-por-reloj-muere-en-un-rebase]] · [[el-cierre-escrito-antes-de-acabar-la-sesion-caduca-en-su-propia-pr]] · [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]]
- **1/2-ago** — #747 (el 32,8% de `clarify` no medía lo que creíamos: agregaba 4 conductas y excluía 5 caminos) · #712 (la raíz recogía `dashboard/test/**` → 38 ficheros corrían **dos veces** por gate) · #758 (el guard de grounding no vigilaba el lead: aprobaba **invertir una negación**) · #760 (SSH del host caído). Y la trampa que más costó: **los arneses dieron falsos por ENTORNO cinco veces en dos días** — endpoint que deriva entre horas, carga >50, `agh_dev` truncada por sesiones paralelas, rama sin rebasar (lo delata `dashboard 439` vs 472) y un control tautológico propio. → [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]] · [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]]

- **21 jul – 3 ago — la base sobre la que corre todo lo de ahora** (cerrado; el día a día vive en `docs/status-log/` del repo). En orden: épica conversacional y drill de voz → la primera comercial nueva rompió el agente en 45 min y salieron 9 issues en un día → el plan de precisión entero en prod (Fases 0-3, eje `query` 72,7 % → 81,8 %) → el rediseño del dashboard (épica #767, cortes 01-04). 👉 **Lo que se lleva ese tramo, y sigue vigente:** cada fix medido contra el modelo real destapa el siguiente hueco, un guard nuevo se mide contra los datos que YA existen, y el gate verde no sustituye una revisión adversarial. Learnings: [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[el-test-que-prueba-el-bug-es-la-traza-real-no-el-golden-del-issue]] · [[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[hitl-turnos-criticos-deterministas-antes-del-llm]] · [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] · [[nul-byte-literal-en-markdown-hace-que-git-trate-el-archivo-como-binario]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]] · [[test-que-reaplica-una-migracion-congelada-estrecha-el-schema]] · [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]]



## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agh-qa-voz-guion-llamada]] (guion de QA en llamada real) · [[agentesia]] · [[top-of-mind]]

_Método de esta semana:_ [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
