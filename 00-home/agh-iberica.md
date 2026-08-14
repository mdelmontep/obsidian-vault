---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-14
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

## Estado (2026-08-14 tarde) — `main` en `5ab5eb8`; **CUATRO PRs mías ABIERTAS** esperando merge de Borja

🟠 **Abiertas (14-ago tarde):** **#1162**/#1152 (la baseline de `verify:ui` se ancla a la COLUMNA, no al ordinal del documento) · **#1163**/#1154 (la firma de `ToneCopys` deja de ocultar el canal — refactor **inerte**: el golden no se mueve) · **#1164**/#1159 (**`GET /version`**: qué imagen sirve prod, por 443 y sin shell) · **#1169** (cierre). Disjuntas entre sí y sin colisión con las 5 ajenas. **Orden si se mergean: 1162 → 1163 → 1164**, la última **con gate detrás**; ⚠️ #1162 toca `dashboard/web/**`, así que **rebasarla caduca su evidencia de navegador** (#934). **5 issues nuevas**: #1161 · #1165 · #1166 · #1167 · #1168.

🔑 **Lo reutilizable de la tarde:** *(a)* **en las TRES la premisa del issue era falsa — y las tres las escribí yo** (ayer 5 de 7, hoy 3 de 3): ya no es mala suerte, es lo que rinde un issue escrito al cerrar sesión sin reabrir el fichero. Y el sesgo **no es solo exagerar**: #1152 **se quedaba corto** (era el ordinal del documento, no el índice de columna → también lo mueve añadir una **fila** al seed), así que arreglar lo que pedía habría cerrado media cosa. *(b)* **Ninguna suite ejecuta `verify-ui.ts`** — control negativo: mutar `VIEWPORTS` de 5 anchos a 1 deja **1140 tests verdes** (→ #1165). *(c)* **`mutate:diff` es ciego a los candados de tipos** → [[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]]. *(d)* **el golden cubre 4 de los 8 métodos**, y detrás vivía un defecto de voz **en prod** (→ #1161): «0 celdas movidas» solo cubre los escenarios que la matriz tiene → [[si-la-variante-se-elige-por-el-contenido-el-candado-por-linea-es-ciego-a-las-demas]].

✅ **Y por fin hay vía para verificar prod sin SSH**, verificada **con la imagen real** (construida y arrancada por primera vez; `migrate.ts` corre dentro): el sello sale del `docker build`, nunca de `process.env` —una env var del panel sobrevive a la imagen— y el contrafáctico de #780 contra el contenedor vivo enseña que **la imagen vieja no puede mentir**. → [[sellar-la-imagen-en-el-build-para-saber-que-corre-en-prod-sin-shell]]

🧰 **En cola para Borja:** **#1126** (una PR apilada no genera run de Actions) · **#1129** (el `git-guard` del repo deja pasar `git reset -q --hard`). ⚠️ **#1036/#1037 caen en `static.ts` con la #1140 de Dani: apilar, no paralelizar.** Y `--delete-branch` **CIERRA** una PR apilada en vez de re-apuntarla → **aplica a #1098**. → [[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]]

🧰 **Herramientas:** `~/.claude/bin/mutate` (4 modos que no miden nada; aborta si el control trajo recuento y el mutante no) y `npm run mutate:diff` en el repo, que **desde el 14-ago cubre `dashboard/`**. → [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]

_Creds:_ `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ espacio final) · SSH del host en `ssh AGH` (el ítem «186» es del PANEL, no de SSH). **`opsa`, nunca `op`**; `item get` exige `--vault`.

## Bloqueantes

- 🔴 **HUMANO, en el panel de Dokploy:** activar el digest en lista con `WHATSAPP_OPEN_THREADS_LIST_PREFIX=hilos_semana` y `WHATSAPP_OPEN_THREADS_LIST_MAX=6`. ⚠️ **El tope es el tramo CONTIGUO aprobado desde 1, no cuántas plantillas hay creadas**: `hilos_semana_7` seguía en revisión y con `MAX=8` un digest de 7 hilos falla el envío entero. Sin las dos envs, #1094 no cambia nada en prod (deliberado).
- 🔴 **DE MANU:** qué hacer con `d.martins`, que recibió tres mensajes con sus hilos. No se ha avisado a nadie.
- 🟠 **DE BORJA:** mergear **#1094** y **#1096**, y en #1096 además **decidir** si se cambia la convención de la línea que todos pegamos.
- ✅ *Cerrados y sin cola: #952 (el digest entregó, 10-ago) · #988 (el teléfono se lee dígito a dígito) · #953 (los 3 hilos pasaron a `delivered`).*
- 🔴 **Prod SIN verificar por contenido**, con una PR de RUNTIME dentro (#1153, `tone.ts`). **Cinco** `ssh -p 5251` con timeout y el sondeo de puertos lo explica: **443 abierto, 5251 sin respuesta** → desde esa salida **solo pasa HTTP(S)**; no es el host ni la credencial, así que las sondas por SSH no existen como vía. ⚠️ **Un 200 no sustituye a esto** (#780) — y el «200 de la app» que se citó tres veces era **el PANEL de Dokploy**: la app es `agente.agh.agentesialabs.com`. 🔧 **La herramienta ya está en la PR #1164**: `GET /version` con la huella fabricada en el `docker build`. En cuanto entre y despliegue → `curl …/version` contra `npx tsx scripts/build-stamp.ts --print` sobre un árbol limpio de `main`. → [[sellar-la-imagen-en-el-build-para-saber-que-corre-en-prod-sin-shell]]
- **Vivas, ya sin PR asociada** (las de la tanda del 7-ago están mergeadas). De la auditoría del 7-ago: **#1031** (el patrón: dashboard client-scoped) · **#1033** (pantalla «Lo mío», espera a #1000) · **#1030** (cancelar hablando; la anáfora en #1038, falta la referencia por cuerpo — cuesta evals) · **#1032** (`addCandidate`: se escribe, nadie lo lee, no se puede quitar) · **#1026** (`llm-smoke` no corre desde que existe) · #1019 · #1020 · #1036 · #1037. **Del 10-ago:** **#1095** (responder al digest no tiene NI UNA eval, y su disparador es un prefijo de texto que nadie asevera) · ~~#1086~~ (CERRADO 14-ago: eran **40 líneas en 15 ficheros** y **tres** importes) · **#1083** (`mutate:diff` no mide lo multilínea — 3 casos en un día) · **#1044** opción A · **#1072**.
- **Decisiones de Borja:** #738 (tolerancia del baseline — **el 22 % del banco no tiene NINGÚN suelo**) · #846 · #847 · #863 · #884 (la confirmación de borrado miente: `tasks … ON DELETE SET NULL`) · **#627** A/B (rec. **B**) · **#929** (`message.text`, toca prompt).
- **Sin dueño y fuera de la cola de arriba:** **#741** (ASR "Grabados"/"Dragados", golden escrito) · **#898** (dos colas de turno por (tenant,usuario), cae en #454).
- ⚠️ **`lastClientId` no caduca NUNCA** y se proyecta como entidad activa cada turno, mientras las oportunidades del mismo array sí pasan el TTL de 30 min → 2ª causa raíz del paso 5 de **#535**, que su caso-oro nº2 no cubre.
- **Rastro de #817/#853:** **#818** (`client.prep` con el agujero que #733 cerró en `client.detail`) · **#820** · **#841** (la ventana que falta degrada en silencio estadístico).
- **#870** — rojo crónico, task.create mete el contexto del mensaje en el título, 0/25 en `main`.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

**Acceso / infra (referencia):** **SSH al host** responde por el **5251** (password del ítem 1Password `ssh AGH` vía `SSH_ASKPASS`; el 22 sigue muerto) → ya usado para las auditorías #747/#668 de esta sesión. Detalle en **#760**. · Secrets de prod → migrar a 1Password (pendiente recurrente).

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

- **13/14-ago (Manu; 13 PRs en dos días)** — el 13 cinco (el arnés se mide a sí mismo) y el 14 ocho, todas de arnés y medición: golden de copia por canal, `verify:ui` que ABRE lo que hay que abrir, el coste de evals en un solo sitio, la línea `pg:` que dice si los `.pg` corrieron, el barrido cubriendo `dashboard/` y el seed produciendo las variantes que las sondas necesitaban. **Lo que sobrevive: en 5 de 7 issues la premisa era falsa y era la que definía el arreglo** — medirla valió más que el parche —, y **dos arneses se validaron solos en su primera PR ajena**. Corolario de método: *una tanda de mutaciones a mano hereda tu hipótesis; el barrido del diff no*. Quedó **sin verificar prod por contenido** (solo pasaba HTTP) → #1159. → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro]]
- **7/10-ago (Manu + Borja; 17 PRs dentro en dos días)** — Borja mergeó las seis de la mañana y Claude las once de la tarde con override de founder. Lo que sobrevive: **el gate verde no es la revisión** (dos PRs devueltas con el gate en verde; su candado pasaba con la regla borrada) · el arnés `npm run mutate:diff` (#1049/#1051), que sobre #1023 señaló los dos hallazgos de la revisión humana **y dos más que no vio** · `agh_dev` estuvo **envenenada** y el remedio escrito estaba incompleto, pasando de «envenenada» a «desfasada» imprimiendo éxito → [[registrar-una-migracion-sin-ejecutarla-envenena-la-bd]] · [[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]] · y **41 runs de Actions de 41 con 0 pasos**, o sea 10 PRs mergeadas con un CI que no ejecutó nada → [[el-rojo-de-ci-tiene-dos-causas-cuenta-los-pasos-ejecutados]].
- **6-ago (Manu; 2 trenes de 6+7 PRs + la auditoría de las 3 llamadas)** — el bypass del HITL (#945) y el sweeper (#953) dentro, más #930/#931/#936; después las 7 issues de voz (#973-#978, #987). Dos lecciones de proceso ya interiorizadas: **avisar ANTES de la primera línea, no antes del mensaje** (tres cruces de avisos en dos días) y que **un candado que existe no es un candado que muerde**.
- **5/6-ago (Manu; tren de 6 + auditoría de voz)** — #920→#926→#922→#924→#928→#932 mergeadas de una en una con gate verde entre cada una. **#926 se estrenó en su propio tren** (desde el 3.er merge el `base` lo pone la máquina) y **el orden salvó ~19 $**: la evidencia de evals se valida por HUELLA de 5 ficheros y ninguna PR previa los tocó, así que sobrevivió al rebase. Criterio reusable: una PR entra **sin re-correr** solo si lo intermedio es solo-docs. Y tres afirmaciones mías refutadas midiéndolas. → [[el-cierre-escrito-antes-de-acabar-la-sesion-caduca-en-su-propia-pr]]
- **5-ago (Manu; 3 PRs + análisis de memoria)** — #896/#892/#890 dentro. El hilo de las tres: **un candado que EXISTE no es un candado que MUERDE** (#881 redondeaba, #753 aseveraba en negativo sin contraparte, #875 no repetía el guard al confirmar). Método que rindió: **revisar mis propias PRs con agentes instruidos para ATACAR mis afirmaciones** — cazó dos errores de contabilidad míos, una copia ambigua y dos ratios medidos a ojo. Y auditando mis propios issues de memoria, dos afirmaciones mías eran falsas y una **cambió el diseño** de #910. → [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[una-senal-cuenta-excepciones-una-tasa-necesita-denominador]]
- **4-ago noche (Manu; 6 PRs + 2 auditorías, tanda final del día)** — #868/#871/#819/#851/#858/#751 mergeadas, #747/#668 cerradas por auditoría. El hallazgo del día: **#851 no necesitaba la superficie nueva que dejaba planteada** — el trade que #851 midió sin salida (prosa-JSON) desapareció al remedirlo bajo tool-calling (#868), 25/25 en los dos lados con una sola frase. Y **#668 corrigió una conclusión propia de #747** con la traza real delante en vez de darla por buena: el "lote de 3 altas ejecutado entero" era falso, había un `store_error` y 4 reintentos — causa raíz real en **#875** (carrera propose→confirm). 4 PRs revisadas y mergeadas por mí mismo (con OK explícito del founder para saltarme la espera a Borja), dos de ellas producto de agentes lanzados en paralelo (cada uno en su worktree). → [[tool-calling-separa-que-herramienta-de-que-argumento-y-puede-romper-un-acoplamiento-de-prosa]] · [[repeticiones-desiguales-por-caso-sesgan-la-tasa-pooled-compara-con-media-por-caso]]
- **4-ago (Manu; 9 PRs mías)** — Fase 3 cerrada (#742), #817 y su cara B #853 dentro, y el instrumento de evals arreglado por dos sitios (#855 hash, #858 1/2 diff por caso). **Lo que se lleva la sesión: cuatro instrumentos mintieron en la dirección que deja mergear**, y `n=10` habría dejado pasar una caída real de 96 % → 48 % (con n=25 salió `24/25 vs 12/25`). Coste de evals medido: caching al 98,5 %, ~11,7 $/corrida. **Y en la segunda tanda, Fase 2B (#868) y #869 (#871)**: la corrida ×3 encontró dos regresiones que el agregado no veía y las dos se arreglaron con código determinista, no con redacciones. → [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[evidencia-fechada-por-reloj-muere-en-un-rebase]] · [[una-suite-de-evals-cuesta-llamadas-por-prompt-mide-el-cache-antes-de-proponerlo]]
- **3-ago (22 PRs)** — Fase 3 en código (A1/A2/A4 + #733; eje `query` 72.7 % → 81.8 %) y cortes 01-04 del rediseño. La lección: **tres de las cinco PRs eran deuda de HARNESS bloqueando producto**, sobre premisas escritas en el repo que nadie comprobaba. → [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]
- **1/2-ago** — #747 (el 32,8% de `clarify` no medía lo que creíamos: agregaba 4 conductas y excluía 5 caminos) · #712 (la raíz recogía `dashboard/test/**` → 38 ficheros corrían **dos veces** por gate) · #758 (el guard de grounding no vigilaba el lead: aprobaba **invertir una negación**) · #760 (SSH del host caído). Y la trampa que más costó: **los arneses dieron falsos por ENTORNO cinco veces en dos días** — endpoint que deriva entre horas, carga >50, `agh_dev` truncada por sesiones paralelas, rama sin rebasar (lo delata `dashboard 439` vs 472) y un control tautológico propio. → [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]] · [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]]

- **13 y 14-ago (13 PRs en dos días)** — todo arnés y medición: golden de copia por canal, `verify:ui` que ABRE, el coste de evals en un sitio, la línea `pg:` que dice si corrieron, el barrido cubriendo `dashboard/`, el seed con variantes. 👉 **Lo que sobrevive:** en **5 de 7** issues la premisa era falsa y era la que definía el arreglo; **dos arneses se validaron solos en su primera PR ajena**; la lista de mutaciones que te DAN no es la objetiva (sale del `git diff`); y `Refs` —nunca `Closes`— cuando entra media issue, comprobado tras el merge. → [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro]] · [[una-herramienta-que-se-aplica-a-su-propio-fuente-necesita-el-rescate-fuera]] · [[closes-N-cierra-el-issue-entero-aunque-escribas-3-de-4-al-lado]]
- **21 jul – 3 ago — la base sobre la que corre todo lo de ahora** (cerrado; el día a día vive en `docs/status-log/` del repo). En orden: épica conversacional y drill de voz → la primera comercial nueva rompió el agente en 45 min y salieron 9 issues en un día → el plan de precisión entero en prod (Fases 0-3, eje `query` 72,7 % → 81,8 %) → el rediseño del dashboard (épica #767, cortes 01-04). 👉 **Lo que se lleva ese tramo, y sigue vigente:** cada fix medido contra el modelo real destapa el siguiente hueco, un guard nuevo se mide contra los datos que YA existen, y el gate verde no sustituye una revisión adversarial. Learnings: [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]] · [[el-test-que-prueba-el-bug-es-la-traza-real-no-el-golden-del-issue]] · [[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[hitl-turnos-criticos-deterministas-antes-del-llm]] · [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] · [[nul-byte-literal-en-markdown-hace-que-git-trate-el-archivo-como-binario]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]] · [[sondear-la-capacidad-real-no-la-presencia-del-binario]] · [[test-que-reaplica-una-migracion-congelada-estrecha-el-schema]] · [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]] · [[un-puntero-durable-a-una-fila-borrada-convierte-un-fallo-en-bucle]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]]



## Preguntas abiertas (para Carlos, no bloquean diseño)

Etapas concretas del embudo comercial de AGH · si el comercial ve solo *sus* clientes (activaría scoping por propiedad, Nivel 2) · números de teléfono para el piloto.

## Seguridad enterprise — 3 escalones RAG

La política de datos del cliente decide el escalón: (1) API pública + DPA + zero-retention; (2) modelo gestionado en tenant UE (Azure OpenAI) — recomendado por defecto en multinacional; (3) on-prem. El dato confidencial cruza el perímetro **en el prompt al LLM** → ahí se decide la seguridad. Migrar entre escalones no implica rehacer el sistema (comparten capa de recuperación). Doc de soporte: `arquitectura-rag-enterprise.html` en el repo.

## Relacionados

[[agh-qa-voz-guion-llamada]] (guion de QA en llamada real) · [[agentesia]] · [[top-of-mind]]

_Método de esta semana:_ [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-de-drift-bidireccional-acopla-las-prs-de-sus-dos-lados]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]] · [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[regiones-distintas-en-el-mismo-fichero-de-test-no-se-afirma-sin-mirar-el-hunk]]
