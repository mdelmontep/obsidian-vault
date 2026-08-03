---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-03
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

## Estado (2026-08-03, noche) — Fase 3 dentro; lo que bloqueaba era el harness

**`main` en `55f4db8`. CERO PRs abiertas.** 22 PRs en la sesión (override de founder; ojo post-hoc de Borja pendiente en todas).

**Eje `query` 72.7% → 81.8%.** Fase 3 con **A1, A2, A4 y #733 dentro**. **#742 sigue ABIERTO a propósito**: A4 entrega el código y su caso del eje **sigue rojo, correctamente** — falta la mitad de prompt. **D15** bloqueado por RGPD. **Fase 2B (#736) sin arrancar** (toca el camino de *todos* los turnos → ventana propia).

⏳ **Las DOS mitades de prompt (A4 + #733) están escritas y SIN aplicar** (PRs #824/#825), para una **sola** corrida de evals.
⚠️ **Trampa para esa corrida:** el eje acepta `from/to/desde/periodo` y el descriptor **sólo honra `range`** → **un caso puede salir VERDE mientras el código degrada**. Mirar **el texto**, no el veredicto.

🔧 **Tres de las cinco PRs de código eran deuda de HARNESS bloqueando producto** (`#806 → #803` · `#808 → A4` · `A4 → #733`). Los dos guards fallaban **por contenido en vez de por contexto**, sobre premisas escritas en el repo que nadie volvió a comprobar. El arreglo bueno **no fue una lista mejor, fue una invariante cruzada** — una lista sólo protege el pasado. → [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]

_Creds:_ 1Password `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ título con **espacio final**). **`opsa`, nunca `op`**; `opsa item get` **exige `--vault`**. ⚠️ El hook salta también si el comando se **menciona en texto** (un `grep`, un mensaje de commit).

## Bloqueantes

- **Decisiones de Borja pendientes:** #738 (tolerancia del baseline — **el hallazgo gordo: el 22% del banco no tiene NINGÚN suelo**) · #741 (umbral: veredicto = 0.75). _(#744, #758 y #762 ya CERRADOS.)_
- **Decisión de LOS TRES (#806, media hecha):** las BD auxiliares ya no se pisan entre worktrees, pero la **`agh_dev` compartida sigue igual** → dos gates simultáneos aún necesitan `DATABASE_URL` propia. La propuesta grande —**una BD por corrida**, medida en **1,3 s** (125 ms crear + 1141 ms migrar), que arreglaría #717/#725 por construcción— sigue **sin decidir**.
- 🔴 **#817 — fidelidad, la que yo miraría primero:** «la semana que viene» se contesta con **ESTA** semana. `matchEnumValue` resuelve por **raíz**, así que entra como `ok` (ni `notfound` ni `ambiguous`): **el resolutor sabe decir cuál de sus valores es, pero nunca «ninguno»**. No falla — **acierta otra pregunta**. Contrato compartido (misma exposición en el descriptor de oportunidad con «la semana pasada») y **reincidencia de #114**, cerrada el 4-jul por otro camino. Con ella: **#818** (`client.prep` con el mismo agujero que #733 cerró) · **#819** · **#820**.
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).
- **#197/#228** (agendar futuro→calendario) — scope Entra `Calendars.ReadWrite` + admin consent (Borja).
- 🔴 **SSH al host CAÍDO** (22 y 5251 sin respuesta, panel y Langfuse a 200 → el host vive). **Causa desconocida, no inventada.** Bloquea leer el texto de los clarify en ClickHouse (#747) y la medición de #741. Vía barata: que Borja pruebe desde su IP. → **#760**
- Secrets de prod → migrar a 1Password (pendiente recurrente).

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

- **3-ago (22 PRs, todo en prod)** — Fase 3 cerrada en código (A1/A2/A4 + #733, eje `query` **72.7% → 81.8%**) y el rediseño del dashboard con los cortes 01-04 dentro (#768-#771 + #812 + el seed #773). **Lo que se lleva la sesión no es el código: es que tres de las cinco PRs eran deuda de HARNESS bloqueando producto**, y las dos premisas que lo permitían estaban **escritas en el repo dándose por buenas**. → [[recurso-de-test-con-nombre-constante-no-aisla-entre-procesos]] · [[un-guard-que-detecta-por-contenido-caza-los-comentarios-que-lo-niegan]]
- **1/2-ago** — #747 (el 32,8% de `clarify` no medía lo que creíamos: agregaba 4 conductas y excluía 5 caminos) · #712 (la raíz recogía `dashboard/test/**` → 38 ficheros corrían **dos veces** por gate) · #758 (el guard de grounding no vigilaba el lead: aprobaba **invertir una negación**) · #760 (SSH del host caído). Y la trampa que más costó: **los arneses dieron falsos por ENTORNO cinco veces en dos días** — endpoint que deriva entre horas, carga >50, `agh_dev` truncada por sesiones paralelas, rama sin rebasar (lo delata `dashboard 439` vs 472) y un control tautológico propio. → [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]] · [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]]

- **31-jul** — plan de precisión entero en prod salvo Fase 2 (#531, P1 #681, P2 #692, Fase 1 #688/#711, P3 #713, #715). Mergeados #720 · #729 (mig 0028) · #730. El flake del gate tenía causa raíz (#717→#718): tres `.pg` re-aplicaban una migración congelada que estrechaba un CHECK, y el `catch` lo disfrazaba de «no hay BD»; mi hipótesis #712 era falsa. → [[test-que-reaplica-una-migracion-congelada-estrecha-el-schema]]

- **21/22-jul — la base que sostiene todo lo de después** (cerrado, detalle en `docs/status-log/` y en el PROJECT-STATUS del repo): épica conversacional #118 (L1/L2a/L2b + anáfora a persona, recall ~100%) · **secretaria #467 completa** (reads fraseados grounded, small-talk, preferencias) · dedup de clientes #245 con `crm.mergeClients` · drill de voz #192 (6 hallazgos) · `ClientIntake` #451 como módulo único de alta · el agente como **2º escritor de `audit_log`** (#485) · self-recipient #482-p1 · módulo temporal único #452 · **épica de arquitectura #457**: gate raíz `npm run gate`, split actor/owner, `createApp` por slices en `src/composition/` (wiring: read/write → `capabilities.ts`, store → `persistence.ts`, env → `config.ts`, worker → `lifecycle.ts`) · Langfuse v3 con rutina de auditoría semanal · #532 (`meeting.update` con `participants` aditivo). Queda de ahí el tramo final de **#454** (switch de `routeTurn`, lane de Borja) y el **smoke conductual del self-recipient** → [[agh-qa-voz-guion-llamada]].

- **31-jul (mañana y tarde, EN PROD)** — el tren entero de la Fase 1 + P2 + P3 mergeado, y **el flake del gate resuelto**. Lo que se lleva la sesión no es el código: son **cinco premisas mías que resultaron falsas** (#688 no toca `capabilities.ts` · el delta de #689 era 3 y no 4 · `response_format` y `tools` **no** se excluyen —abarata la Fase 2 entera— · #712 no era doble ejecución · y #718 impedía envenenar pero **no curaba** lo ya envenenado, que encontró Borja → #729). Y un detalle de método: **fue #700 lo que hizo observable** el flake de #717 — antes salía PASSED. → [[test-que-reaplica-una-migracion-congelada-estrecha-el-schema]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[nul-byte-literal-en-markdown-hace-que-git-trate-el-archivo-como-binario]]
- **30-jul (noche/noche-2, en PR)** — **Fase 1 mitad de código** (#688: los reads que faltaban) y **P2** (#692: el guard de clasificación del presentador). Y la **primera corrida del eje**: el `0/27` importa menos que lo que dijo — **6 de 9 preguntas fuera de superficie rutan a un target REGISTRADO** con el filtro ausente (pides recordatorios y te da tareas; preguntas qué cerraste y te da lo abierto), así que el frente ciego es **invisible en prod**. De ahí #698, y el descubrimiento de que el eje no medía `threads.open` (#697/#699). Además #700 (#686): los `.pg` del dashboard contaban como PASSED sin BD — y el candado, por escanear los DOS proyectos, encontró que el agente también lo tenía. → [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]] · [[el-caso-que-mide-un-hueco-entra-antes-que-la-capacidad]] · [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]] · [[un-guard-nuevo-se-mide-contra-los-datos-que-ya-existen]]
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
