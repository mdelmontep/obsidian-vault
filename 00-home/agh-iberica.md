---
title: agh-iberica
date: 2026-07-02
updated: 2026-08-01
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

## Estado (2026-08-01, mañana) — la medición no era fiable, y eso reordena el plan

**`main` en `c98186c`.** **11 PRs abiertas, todas nuestras, todas verdes y rebasadas** (verificado una a una). Orden: `#579 → #737 → #743 → #739 → #740 → #746 → #750 → #755 → #757 → #759`, y **#762 (solo-docs) se mergea ya**. ⚠️ #759 va **detrás de #737** (add/add en el enum de `messages.ts` → combinar).

🚨 **La medición no es estacionaria.** Mismo commit, payload idéntico, `temperature: 0` → **0/5 fallos a las 19:00, 3/5 a las 00:40**. `MODEL_ID=gpt-4o` es el de prod: **el agente rutea distinto según la hora**. Invalida comparar corridas de momentos distintos y el baseline de hace semanas. → [[medir-un-cambio-contra-un-llm-entrelazado-no-en-bloques]] · #738 · #748

**Eje `query` 72.7%.** Fase 2A (#737) y Fase 3-A2 (#743) listas sin mergear. Lo que queda —A1/A4 (#742) y Fase 2B (#736)— son cambios de prompt: **no se tocan sin el arnés** (PR #750).

**Tokens (#736):** `SYSTEM_PROMPT` = 13.073 tok = **99,6% del input**; tipar sale **+3,7% más caro** → 2B se justifica por corrección, no por ahorro.

**Auditoría (3 agentes):** #751→#757 · **#752 arreglado dentro de #737** · #753 (8/15 en #755; los 2 de `dashboard/auth` son de Borja) · #749→#750, ya **verificada end-to-end con llamadas reales**.

**Panel adversarial de 4 decisiones (20 agentes): me corrigió en TRES.** La decisiva, #752 — mi llave (`signals`) cubría la mitad de los caminos, así que habría cerrado el issue en verde con el bug vivo. Detalle en cada issue.

**#747 → PR #759:** el 32,8% de `clarify` **no medía lo que creíamos** (agrega 4 conductas, excluye 5 caminos que también piden algo). Señal `asked`, 8 razones. Y el punto único de salida del brain ya no **sobreescribe** las señales de las ramas internas.

**Issues nuevos hoy:** **#758** (el guard de grounding no vigila el lead: aprueba **invertir una negación**; y `tasks` tiene el mismo defecto sin nada que lo tape) · **#760** (SSH del host caído) · **#761** (3 asserts anchos que quedan). → [[una-etiqueta-nacida-de-un-caso-concreto-sobrevive-a-su-contexto]]

_Trampa nº1 del entorno:_ **los cuatro arneses (evals, gate, `.pg`, y el gate otra vez) dieron falsos por ENTORNO en dos días** — endpoint que deriva · carga >50 (load 32 → 16 rojos que en limpio pasan) · `agh_dev` truncada por sesiones paralelas · **rama sin rebasar** (lo delata `dashboard 439` en vez de 472). Descartarlas antes de mirar el diff. → [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[test-db-persistente-contaminada-entre-ramas-recrear-fresca]]

_Creds:_ 1Password `AGH Iberica` → `Open AI AGH` **por ID** (⚠️ el título lleva **espacio final**). Con dos cuentas en `op`, **`op signin` exige `--account agentesialab.1password.eu`** o falla con «multiple accounts found». El ítem `Langfuse AGH` es **login web, NO API keys** → leer trazas por HTTP necesita navegador; las keys viven en el env del contenedor (→ SSH o panel). SSH del host por `askpass` con `op` inline — **`ssh-copy-id` NO funciona** (el host no acepta password de root). → [[op-read-secreto-nunca-en-comando-bash-ni-desde-memoria]]

## Bloqueantes

- **Decisiones de Borja pendientes:** #744 (compartir la credencial del gateway) · #738 (tolerancia del baseline — **el hallazgo gordo: el 22% del banco no tiene NINGÚN suelo**) · #741 (umbral: veredicto = 0.75) · **#758 (A: el presenter deja de recibir el lead · B: el guard exige el orden)** · #762 (mergear la regla).
- **L5/L3-A** — bloqueados por RGPD (política de datos con el cliente, decisión Borja).
- **#197/#228** (agendar futuro→calendario) — scope Entra `Calendars.ReadWrite` + admin consent (Borja).
- 🔴 **SSH al host CAÍDO** (22 y 5251 sin respuesta, panel y Langfuse a 200 → el host vive). **Causa desconocida, no inventada.** Bloquea leer el texto de los clarify en ClickHouse (#747) y la medición de #741. Vía barata: que Borja pruebe desde su IP. → **#760**
- Secrets de prod → migrar a 1Password (pendiente recurrente).

⬇️ _Debajo de esta línea: historial, referencia y contexto de negocio — no se paga al arrancar una sesión._

## Historial reciente (condensado — detalle en `docs/status-log/` del repo)

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
