---
title: agh-iberica
date: 2026-07-02
updated: 2026-07-29
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

## Estado (2026-07-29) — el lote a prod, dos residuos de infra y un bug cazado en vivo

**`main` en `87a3d00`, todo desplegado.** Borja mergeó su lote (#628/#629/#630) **arreglando antes los 3 hallazgos serios** de mi revisión del 28, cada uno con rojo reproducido. Aviso de coordinación real: cuando leí Slack, el canal iba **por detrás del repo** — el lote ya estaba mergeado y el mensaje no había salido.

**Mías, 3 PRs con override de founder documentado:**
- **#636/#637** — los dos residuos que Borja encontró en #632. El primero era **mi propio fallo un escalón más abajo**: sondar `docker compose version` sigue mintiendo si el *servicio* del compose está parado → la sonda pasa a ser el comando exacto. Y `DRIFT_PG_PORT` aplica a los **dos** modos, porque `migrate.ts` corre en el host → [[sondear-la-capacidad-real-no-la-presencia-del-binario]].
- **#638/#639** — `graph-calendar-client` nacía mudo; `graphErrorCode`+`logGraphRejection` a `graph-errors.ts`. Peor que en correo: los reads de agenda son best-effort, así que un 403 de scope **se veía como agenda vacía**.
- **#640/#641** — bug **de prod cazado mientras ocurría**, y **nombrado por la instrumentación de #628** (`errorClass=store_error`): el dedup del alta miraba la cartera del owner y el índice único es de tenant → `23505` crudo. Raíz de método: la normalización estaba escrita **dos veces en dos lenguajes** → [[guard-en-codigo-que-predice-un-indice-unico-de-sql-diverge]].

**Sin código, con decisión encima de Borja:** **#580** triado a `ready-for-human` — el PATCH de Graph tiene dos trampas oficiales (el `body` **mata el enlace de Teams**, `attendees` se **reemplaza** y avisa a los borrados) y recomiendo resolver contra el calendario en vez de tabla espejo → [[patch-de-evento-en-graph-reemplaza-attendees-y-puede-matar-el-enlace-de-teams]]. · **#591 MEDIDO**: nuestro tramo es **el 28% del p50 de voz**, el resto es STT/TTS/red → tocar el brain no arregla esa latencia; y el desglose fino **no es medible** sin spans → [[antes-de-optimizar-latencia-mide-tu-tramo-y-restalo-del-e2e]].

**#624 sigue abierto, pero más acotado:** #628 está en prod (verificado) y el token de Borja **se refrescó el 28 a las 11:06 UTC, antes del fallo y vigente** → el refresh funcionaba, el peso se va a las dos hipótesis de Graph. **Solo falta que alguien dicte un correo**: el log únicamente se escribe en el instante del rechazo. Anotado: `m365_credentials` no guarda los scopes concedidos — con el `scp` se resolvería sin repro.

**Accesos (ya no hay que redescubrirlos):** SSH al host va con el ítem 1Password **`ssh AGH`** (el ítem «186» es el del PANEL, `:3000`) y el host **no acepta password de root para `ssh-copy-id`**. **Langfuse es self-hosted en el mismo host** y su ClickHouse se consulta **sin credencial** desde el server — vía práctica para medir trazas.

**A humano:** licencia/buzón M365 en Entra (#624) · el correo dictado · ojo post-hoc a la copia de #640 y su fork B · enfoque de #580 · A/B de #627 · **#579 de Dani sigue abierta, limpia y sin que nadie la mergee** · `RETELL_WS_SECRET` sigue sin definirse en prod.

## Estado (2026-07-28) — fallo de `email.send` en prod + revisión cross-PR con Postgres real

**`main` en `5577b07`.** Dos frentes el mismo día.

**Frente de Borja — `email.send` ROTO en prod** (determinista, repro en vivo; último borrador OK el 21-jul 14:41 UTC). Diagnóstico sobre trazas Langfuse reales → 4 issues y 3 PRs **sin mergear**: **#628** (#624 observabilidad), **#629** (#625 batch parcial) y **#630** (#626 🔴 el drafter *inventa valoraciones y compromisos* que salen a un tercero). **#627** a humano. El hallazgo que importa de #624: el `errorClass` se calculaba pero `inbound-pipeline` proyectaba solo `{kind,status}` y el error de Graph moría en un catch sin log → **la causa exacta no es determinable con la instrumentación actual**, y no se fabricó.

**Frente mío — revisión, no implementación** (no había ni un issue `ready-for-agent` libre). Tres agentes de expertises dispares sobre las 4 PRs abiertas, con los hallazgos serios **verificados a mano antes de publicar**:
- **Gate con Postgres 16 nativo**: las cuatro integran **sin un solo conflicto en cualquier orden**, `agente 1990/208/3 · dashboard 322/0/0 · drift ok`. **Deuda de skips pagada: 42 ficheros `*.pg.test.ts` → 184/184, 0 skips** — Borja las cerró con ~343 en skip porque su 5433 lo ocupaba otro proyecto → [[e2e-smoke-skip-honesto]].
- **3 serios publicados**: el «enum cerrado» de #628 no lo está en código (el `payload` puede ser **salida cruda del LLM** → texto libre a la traza aunque `traceContent` esté off); en #629, el fallo M365 sigue diciendo «lo reintentamos» con el pending vacío **y el test nuevo cementa el bug** con un `toBe` de identidad; y el rótulo vuelca cuerpo de nota y PII en **24 de los 25** kinds, saliendo por el altavoz pese a `reviewChannelFor`. Todos con la misma raíz de método → [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]].
- **Verificado limpio** lo que se temía: el candado del regex de `error-classifier` intacto, sin fuga de PII por propagación, y el solape `graph-mail-client.ts` (#628 ∩ #579) **combina sin filtrar direcciones**.
- **#632 → PR #633 (`66026f4`)**, lo único que escribí: el drift-gate sondeaba el binario `docker`, no un Docker usable → [[sondear-la-capacidad-real-no-la-presencia-del-binario]].
- **#579 de Dani desbloqueada**: mi aviso del 27-jul de que conflictuaría **era falso**; la rebasó el 28-jul 13:27 y no tiene ni un conflicto. Un aviso de conflicto caduca y se vuelve bloqueo fantasma.
- Gotcha: el issue no se autocerró porque la PR decía «Cierra #632» → [[keywords-de-cierre-de-github-solo-funcionan-en-ingles]].

**Orden de merge sugerido:** #628 → #630 → #629 → #579 (radio de impacto; sin dependencias duras).

**A humano, con dueño:** **licencia/buzón M365 en Entra** — *lo único que cierra la causa raíz de #624*; la llamada que falla es `POST /me/messages` con `Mail.ReadWrite`, 880 ms → primer intento, y hay **2ª hipótesis** además del trial caducado: el admin consent de un scope nuevo puede no auto-propagarse (`oauth-flow.ts:38-42`, gotcha #143). Los separa el código de Graph: `MailboxNotEnabledForRESTAPI` 404 = licencia · `ErrorAccessDenied` 403 = consentimiento. · ojo al prompt de #630 · **#590/#591 (voz)** siguen esperando desde el 26-jul · A/B de #627.

## Estado (2026-07-27) — call real: 13 fallos → 25 PRs mergeadas, todo en prod

**`main` `3f674a0`.** De una llamada de voz real de Manu (`call_530a8af9…`, 25-jul, 6m28s, **terminó colgando en un bucle**) salieron 13 fallos + 3 rondas de fixes-de-los-fixes. **Corrigió el diagnóstico del 22-jul**: no era solo capa de voz, había fallos de brain/datos reales — el recall negaba una reunión que el propio agente acababa de crear ([[escribir-en-una-fuente-y-leer-de-otra-hace-que-el-agente-se-contradiga]]), la negación no mataba el pending, el ruido de ASR se daba de alta como cliente, el desborde mandaba 1 ficha de 3 en silencio. Conversación medida: **35/43 → 40/45**. Después se barrieron los issues LIBRES corregibles (#532, #619, #540, #601) y se resolvió **#521** de verdad (ordinales contra la última lista, en código determinista, cero egress).

**Lo más valioso, y es de método:** medir contra el modelo real **DESPUÉS** de mergear destapó tres huecos que los tests verdes no veían → [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]]. Y el arnés de smoke daba **falso verde** con asserts de eco → [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]].

**Gotchas que costaron caro:** [[pr-encadenada-se-mergea-en-su-base-si-no-borras-la-rama]] · [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]] · [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]]. Runbook nuevo: gate sin Docker (pg16+pgvector por Homebrew); **dos gates simultáneos contra el mismo 5433 = falso negativo**.

Detalle día a día: `docs/status-log/2026-07-27-*.md` del repo.

## Estado (2026-07-22) — cerrado

`main` al día y sin PRs propias al cerrar. **#532 CERRADO** (meeting.update `participants` aditivo; `topics`/`nextAction` siguen sustitutivos por contrato de #520). Round 2 de stress-testing dejó **PR #581** (#567 `meeting.schedule` gana participants+durationMinutes) y **PR #582** (#569 valor relativo de oportunidad ya no guarda `"20%"` literal), ambas aún abiertas; **#580** separado (add-after en M365, precisa PATCH de evento Graph). Dani: **PR #579** (#568 email cc), evals ×3 corridas por Manu → verde. Borja cerró su cola: #557 mergeado, #537/#558 reconciliadas, ojo post-hoc F2/F3 sin hallazgos. Gotchas de sesión: [[background-bash-io-bound-se-mata-solo-reintentar]] · [[subagente-background-bash-no-se-autorreanuda-esperando-notificacion]].

## Estado (2026-07-21) — PROD VIVO · secretaria + audit + self-recipient + coherencia prompt + BORRADO de entidades sueltas (5) + fixes de dogfooding

Demo del 7-jul con Carlos OK. CI Actions muerto por billing → **gate LOCAL** `npm run gate`/`gate:full` (lint 0-`any` + typecheck + test agente + gate dashboard [+ drift]) sobre HEAD rebasado, documentado en cada PR; **merge = Borja** (`gh pr merge --admin`, el rojo de Actions es falso negativo) o **founder override nombrando el bypass por-PR** (el clasificador lo exige; ver [[agh-self-merge-clasificador-nombrar-bypass]]). El detalle día-a-día vive en `docs/status-log/` del repo y en [[archive-completed]].

**Agente conversacional — todo en `main` + prod (autodeploy):**
- **Capacidad conversacional (épica #118)**: L1 ventana de turnos → L2a recentEntities → L2b fuente única de entidad activa + #445 anáfora a persona. Recall ~100%, OVERALL ~98-99%. **L5/L3-A POSPUESTOS por RGPD** (Borja): sin egress de nombres de cartera al LLM hasta cerrar la política de datos con el cliente.
- **Dedup de clientes #245 CERRADO**: `crm.mergeClients` (fusiona duplicados sin perder historial, transaccional) en prod + fusionado el duplicado real del drill (`grabados`→`Dragados`). Scanner read-only `scripts/scan-duplicate-clients.ts`.
- **Drill de voz #192**: 6 hallazgos mergeados (lastVoicePointer, HITL de voz, recap inventado, saludo≠siembra, puntuación ASR, sí/no desnudo).
- **Secretaria conversacional (épica #467) COMPLETA**: P1 reads de lista fraseados grounded (voz intacta, kill-switch `READ_PRESENTER_ENABLED`) + P2 social/small-talk + P5 preferencias firma/franja (`user_preferences`, mig 0016). PRs #471/#473/#474. Ver [[agh-secretaria-conversacional-plan-1-2-5]].
- **#451 `ClientIntake`** (#484): módulo único de alta (normalización + dedup exacto/aproximado 0.85 + `confirmedNew` + email→update); `CreateClientWriteExecutor`→adapter retrocompat; **onboarding gana el dedup aproximado**.
- **Gaps de la auditoría Langfuse**: #481 bucle del «sí» al conectar M365 (#494) + #482-p2 guard del `to` (no placeholder/pronombre al HITL, #491).
- **#485 audit del agente (#501, `365c1e9`)**: el agente = **2º escritor de `audit_log`** — cada write CRM mutador (client/contact/meeting+note/task + borrado del duplicado en mergeClients) en la MISMA tx que la entidad, forma dashboard (#440/#450), actor=`ctx.userId`, **procedencia** (voice/onboarding/chat) en el `after` — sin columna nueva ni migración (solo comentario en schema.sql → drift no aplica). `AuditStore` (Postgres/InMemory/Noop) + `tx?` en los stores + `ClientStore.findById` (FOR UPDATE) + `delete` con RETURNING. 4 pg-real de atomicidad (incl. rollback). Patrón reusable: [[audit-log-multi-escritor-procedencia-en-after-before-sin-carrera]].
- **#482-p1 self-recipient (#503, `0c40fdf`)**: «mándamelo a mí» → resuelve `users.email` (poblado por `provisionWorker` + el connect de M365 que captura el claim `email/upn/preferred_username` del id_token, best-effort/fail-closed, sin persistir el token); guard anclado que nunca secuestra un envío a terceros; señal en `SYSTEM_PROMPT`; fallback `awaiting_email` en onboarding. Cierra #482 de verdad (estaba CLOSED sin la parte 1 hecha).
- **#452 módulo temporal (#509, `4be24b9`)**: la semántica temporal (`parseWhen`/`formatLocal`/tz) estaba duplicada en 3 executors (meeting.schedule/reminder.schedule/thread.postpone) → consolidada en `src/reminders/when.ts` (`resolveTemporal(nowMs,when)→resolved|past|invalid` + `formatLocalInstant`). Move-don't-reshape (cero cambios de wording), +21 tests DST. Cierra el hallazgo 3 de la revisión #457.
- **#508 fix del harness (`6685712`)**: `git-guard` ignora el contenido entre comillas antes de matchear → un `gh pr create --body "…reset --hard…"` o `git commit -m "…"` ya no dan falso positivo (mismo fix al hook global `~/.claude/hooks/git-guard.sh`).
- **Auditoría de COMUNICACIÓN (14-jul noche, 5 lentes sobre 441 trazas Langfuse)** — verificada contra `main` actual (el corpus era pre-fix → casi re-fixeo 3 bugs ya resueltos; ver [[verificar-que-el-bug-sigue-vivo-contra-codigo-actual-antes-de-fixear]]). En prod: **#511/#515** (breaker del clarify en bucle — repregunta idéntica ×3 → menú de capacidades; honra #175; mig **0020** `clarify_repeat`) · **#514/#516** (`client.prep` «prepárame lo de X» = briefing prospectivo: última reunión + oportunidades + tareas + cita de hoy M365) · **#522/#524** (`note.create` = nota suelta por voz, superficie propia; evals ×3 routing 15/15). **PR #519 ABIERTA** (cita FORWARD en `client.prep`, `CalendarTool.upcomingDays`) → **revisión de Dani** (zona m365). Cerrados por análisis: **#512/#513** (ya resueltos por #232/#231), **#523** (dips de evals = oscilación + timeouts de gateway), **#525** (read-through 32/32, la regla ya existe). **Backlog vivo en zona de Borja:** **#520** (corregir «lo último» no-solo-cliente → `case correct`/`confirm` = tramo de #454) y **#521** (deícticos/ordinales «el último» = fork de diseño: revierte el voz-only de #247). No rammear zonas activas de compañeros: [[no-defaultear-a-conservador]].
- **Observabilidad**: Langfuse v3 en prod (tracing activo, content=true); `userId` en claro opt-in `LANGFUSE_TRACE_PLAIN_USER_ID` (#472/#475); **rutina de auditoría semanal** (lunes 09:00, maker/checker, postea como bot; idempotente por estado de issues — ver [[audit-bot-recurrente-idempotencia-por-estado-de-issues]]).
- **Arquitectura (épica #457)**: gate raíz `npm run gate` (#453); split actor/owner (#450); `createApp` por slices en **`src/composition/`** (#455) — **wiring nuevo: tool/read/write → `capabilities.ts`, store → `persistence.ts`, env/validación → `config.ts` (⚠️ orden de throws fijado por `app-config.test.ts`), worker → `lifecycle.ts`; NUNCA `app.ts`**; smoke contra el brain real (#456, `LlmBrain` retirado).

**Dashboard CRM** (#296, Borja/Dani, prod `panel.agh.agentesialabs.com`): épica premium #392 CERRADA; escrituras en ficha (#439) + split actor/owner (#450) + CRUD de cliente completo (#305) + UI ficha/cartera (#483, mig 0017 `tasks.due_date`). En curso #490/#493 (editar/borrar notas/reuniones/tareas + pulido). Vínculo identidad dashboard↔agente vía `oid` de Entra (#489, PR #492). Zona dashboard-local, cero cruce con el agente salvo `schema.sql`.

**Migraciones al día: 0021** (`conversation_state.last_write`, #527). 0016 `user_preferences`, 0017 `tasks.due_date`, 0018 `users.email`, 0019 `tasks.meeting_id` (Borja, #502), 0020 `conversation_state.clarify_repeat` (#515).

**Follow-ups (no bloquean):**
- **#500 (Borja)**: superficie de **visualización del `audit_log`** en el dashboard, ahora que incluye los writes del agente con procedencia. Read-only, sin migración.
- ~~**Backfill de `users.email`**~~ HECHO 2026-07-14 (`UPDATE 4` en prod: david/estefanía/itziar/jamie desde su identidad `entra-invite`, verificado read-only antes; guardado `email IS NULL`+`entra-invite`+`LIKE '%@%'`). **Carlos + 6 usuarios test** siguen sin email (sin `entra-invite`) → se capturan al conectar M365 o vía `awaiting_email`. Falta smoke conductual E2E del self-recipient (dictar «mándamelo a mí»).
- **Arquitectura (#454, lane de Borja)**: queda el tramo final (transiciones del pending en el switch de `routeTurn`, `hitl-brain.ts`), exige ventana propia + anuncio. **#520 ya MERGEADO en ese mismo switch (`case confirm`/`correct`, mig 0021) → #454 debe REBASAR sobre el `main` nuevo antes de seguir** (opción A, decisión de founder). Considerar **#521** (deixis/ordinales — fork de diseño del voz-only de #247) y **#535** G1/G2 (confirm+composición · limpieza tras write fallido), que caen en el mismo switch → mismo window; el test-candado #536 ya protege el invariante del failed-confirm (si el refactor mueve el sello antes de `executeWrite`, salta en rojo).
- **Smoke conductual E2E** del self-recipient (dictar «mándamelo a mí» por WhatsApp/voz) + carlos+6 test sin `users.email` (reconexión M365). → guion completo de QA en llamada: [[agh-qa-voz-guion-llamada]].
- **En prod 2026-07-15**: #519 (cita FORWARD en `client.prep`, mergeado) · #520/#527 (corregir «lo último» confirmado para reunión/tarea/oportunidad/contacto, no solo cliente; nuevos `meeting/task/contact.update` + puntero `lastWrite`, mig 0021).
- **En prod 2026-07-16**: #529/#530 (`cc233ac`) — coherencia del `SYSTEM_PROMPT` (catálogo `capabilities` completo, regla única «apuntar», `email.send` en sub-viñetas, `#231` consolidado) + composición multi-write explícita (política pro-precisión) con ejes de eval `composition`/`confusion`. El modelo YA componía → blindaje, no fix (foto ×3): [[prompt-coherencia-fotografiar-evals-antes]]. Pendiente ojo post-hoc de Borja a F2/F3.
- **En prod 2026-07-20**: #536 (`692b73a`) — test-candado del failed-confirm (#535). La auditoría-langfuse semanal filó #535 pero **la hipótesis no se sostiene contra `main`** (un write fallido == excepción; el `catch` corre antes del sello de estado, ya limpio); el test ancla ese invariante y blinda la zona de #454. **G1** (confirm+composición) y **G2** (limpieza de estado tras write fallido) = forks de diseño `ready-for-human` → ventana de #454. Verificar-contra-main: [[verificar-que-el-bug-sigue-vivo-contra-codigo-actual-antes-de-fixear]].
- **En prod 2026-07-21 — jornada de dogfooding real (11 PRs, `main` `9471b07`):** **borrado de entidades sueltas** (reunión/tarea/oportunidad/contacto/nota) por anáfora «bórrala» (vía `lastWrite`) y por referencia «borra la reunión de X» + audit (#545/#546/#547/#548); «bórrala» sobre un borrado PENDIENTE lo confirma (#549, antes el LLM lo cancelaba → casi borra lo que no era). **Precisión del interpreter:** alta de cliente con contexto NO fabrica reunión fantasma (#543); apunte con día = `reminder.schedule` con body limpio (#551). **Correos como secretaria** (#552, EmailDrafter). + enlace M365 en `seeding` (#539), `opportunity.create` no revienta por stage fuera del embudo (#542). Método+patrones nuevos: [[hitl-turnos-criticos-deterministas-antes-del-llm]] · [[guard-en-prepare-de-un-item-declina-el-batch-entero]]. **A la cola de Borja (zona #454, NO auto-merge):** **PR #557** (#535-G1, «sí, y además X» → confirma pending + encola compuesto, orquestado en `handleSerialized` sin tocar el switch) · **#521** (deixis «la última reunión», fork de diseño = revertir voz-only de #247). Follow-up: auditar `opportunity.create` (su store.create sin `tx`). Decisión de reuniones (founder): futura→schedule, pasada dictada→create, alta de cliente→ninguna.

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
