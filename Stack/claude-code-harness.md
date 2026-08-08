---
title: Claude Code — harness, loops y automatización
date: 2026-07-12
source: CLAUDE.md global (sección "Loops y harness" movida aquí para descargar contexto)
tags: [claude-code, harness, loops, automatizacion]
---

# Harness, loops y automatización

Detalle operativo; el resumen vive en el CLAUDE.md global. Ver también [[claude-code-gotchas]].

## Dos ejes, no una escalera (3-ago-2026)

La escalada `prompt → /loop → /schedule → Workflow` mezcla dos preguntas independientes.
Separarlas evita el error caro: montar un loop donde tocaba un grafo, o al revés.

| | Pregunta | Piezas |
|---|---|---|
| **Tiempo** | ¿cuántas VECES se ejecuta? | una (prompt) · N con gate (`/loop`) · N sin ti delante (`/schedule`) |
| **Topología** | ¿cuántos AGENTES dentro de una vez? | uno (prompt) · varios con reparto fijo (`Workflow`) |

Se combinan: un loop cuyo cuerpo es un grafo es normal, y caro. Un grafo suelto sin loop
también. Meter un cuerpo mejor en un reloj sin gate no arregla el reloj.

## ¿Vale la pena un loop?

Solo si se cumplen los 4:
1. La tarea repite al menos semanal.
2. Algo puede rechazar el output automáticamente (test, lint, build, regla dura).
3. El agente puede cerrarla end-to-end sin devolverte la mitad.
4. "Listo" es objetivo, no de criterio.

Si falta uno → prompt manual.

**La prueba de la cuenta atrás.** Un loop CONVERGE; no descompone, no explora, no decide.
¿El rojo del gate baja de forma monótona? "23 tests fallan → 19 → 14" es un loop. "La feature
funciona: no / no / no / sí" no lo es: es un reintento caro con supervisión intermitente.
En implementación grande el fallo típico es ese — el problema no es "el output fue rechazado,
reintenta", es "todavía no sé qué significa terminado", y a eso no se le pone gate.

Sí son loop: suite roja→verde (el gate cuenta fallos), migración sobre N llamadas (cuenta
sitios sin migrar), matar flaky tests, cerrar issues ya escritas de una en una.
Para lo grande la secuencia es otra: descomponer (`/prd-to-issues`) → grillar la
DESCOMPOSICIÓN, no el código (`/grill-me`) → construir issue a issue, y ahí sí un loop por
issue → grafo solo donde hay abanico real.

**Orden de construcción:** manual confiable → skill → loop (con gate) → schedule. Nunca schedulear algo que no probaste a mano.

## ¿Cuándo grafo?

Las tres a la vez; si falla una, no es grafo:

1. **Las piezas no se hablan entre sí.** Seis lentes de auditoría, cinco enfoques compitiendo.
   "Lee el schema → escribe la migración → corre el test" es una cadena, no un grafo.
2. **Quieres perspectivas que un solo contexto no puede tener a la vez.** La independencia de
   contexto es lo único que compra un grafo y un prompt largo no. El que escribió el código es
   mal juez de ese código.
3. **El reparto lo decides tú.** Si te da igual, deja que Opus 5 orqueste subagentes solo, que
   ya lo hace bien. El grafo se paga cuando la topología es una decisión que quieres idéntica
   cada vez: dos refutadores siempre, jueces en Opus siempre, tope de ocho siempre.

**El grafo NUNCA es el checker.** Puede ser maker, diagnóstico cuando el gate falla, o
explorador. El veto lo tiene siempre algo determinista. Un panel de jueces LLM como condición
de parada es un agente autoaprobándose con quórum: más caro y más convincente, igual de ciego.
Dentro de un loop, dispararlo condicionalmente —cuando el gate determinista ya falló—, nunca
en cada iteración: 6 lentes × 8 hallazgos × 2 jueces son 96 agentes por pasada.

Implementación de referencia: `~/.claude/workflows/audit-graph.js`, lanzable con `/audit-graph`.

### Y CUÁNDO no: el alcance se decide por lo que cambió (3-ago-2026, TuCRMIA)

La regla con la que se venía disparando era de calendario —«cada 3-4 issues cerrados»— y esa
regla **no sabe mirar el trabajo**: manda seis lentes contra un árbol donde puede que nadie
haya tocado una hoja de estilos ni una migración. No es más riguroso: es más caro, tarda más y
su informe se lee **peor**, porque el hallazgo real se pierde entre confirmaciones de lo que ya
estaba bien. Un informe que enseña a saltárselo es P5 con otra ropa.

- **Cada lente declara su TERRITORIO** (globs) y corre solo si algo de ese territorio cambió
  desde la última auditoría **registrada**. Si no cambió nada de ninguna: no hay auditoría.
- **El territorio es generoso, y no es el diff.** Estas auditorías buscan fallos en las JUNTAS,
  y una junta se rompe desde cualquiera de sus dos lados: tocar la API puede romper su
  composición con el panel sin que el panel cambie. Recortarlo al diff la convierte en una
  revisión de diff, que ya hace el gate.
- **Una lente que NUNCA ha corrido entra aunque su territorio no haya cambiado.** «¿Ha cambiado
  algo desde la última vez?» da por hecho que hubo una última vez; para una lente nueva su
  territorio está sin mirar entero. Apareció a los diez minutos de escribir el registro.
- **El guion se PARA sin alcance.** Ante la duda no audita todo: eso es el calendario otra vez.
- **Registro en el repo** (`docs/plan/auditorias.json`): commit, fecha, lentes, hallazgos. Se
  escribe DESPUÉS de correr, nunca antes, o el árbol dice que se miró algo que nadie miró.

Implementación: `scripts/auditoria-alcance.mjs` + `.claude/workflows/auditoria-composicion.js`
en TuCRMIA. Con test de que un cambio de CSS dispara la lente de interfaz **y ninguna más**: su
primera versión reclamaba todo `src/` para la lente de ramas mudas, o sea el mismo despilfarro
que venía a corregir.

### Reparto de modelo dentro del abanico, y el barrido de effort (3-ago-2026)

- **Opus busca y sintetiza; Sonnet refuta.** La refutación es el eslabón de VOLUMEN y su
  trabajo es acotado: abrir el fichero y ver si la afirmación se sostiene. El juicio —qué es
  grave, qué duplica a qué— se queda en Opus.
- **Tope declarado, y lo que queda fuera se NOMBRA.** Sin él, 6 lentes × N hallazgos × 3
  escépticos se va a ~150 agentes sin que nadie elija ese número. Lo no refutado se reporta
  como «ni confirmado ni descartado», jamás en silencio: un tope callado se lee como «lo
  miramos todo».
- **Dos refutadores, no tres, y matar exige que los DOS refuten.** El error cae del lado de
  dejar vivo un falso positivo antes que de enterrar un hallazgo real; el filtro fino es la
  síntesis.
- **Buscadores a effort `medium`: NO se pierde profundidad.** Medido con 64 hallazgos: los
  supervivientes traen reproducción ejecutable, fichero:línea y la comprobación de qué otra
  capa podría salvarlos. Lo que falta con `medium` es **cobertura**, no calidad. La palanca no
  es subir a `high`: es subir el tope de refutaciones.

## El GOAL

No es una alternativa a loop ni a grafo: es lo que hace el loop TERMINABLE. Sin él no hay
parada, hay agotamiento.

**La prueba: un comando con exit code decide si es verdad.** No tú leyéndolo, no el modelo
evaluándose. Si no puedes escribir ese comando, no es un GOAL, es una intención.

Y el gate tiene que medir la condición, no un proxy suyo. Caso real (cryptobruj, 3-ago): el
GOAL pedía "≥10 reglas verificables" y el gate era `grep -c "##"` — ocho encabezados vacíos lo
pasaban. Ni siquiera hace falta que el modelo quiera hacer trampa: el gate ya la regala.

**La guarda tiene que estar en la capa que ejecuta, no solo en la que teclea.** Un hook de
Claude Code protege de lo que escribe Claude. No protege del operador, ni del panel de
Dokploy, ni de un `docker exec`. En cryptobruj la cadena acabó siendo tres capas
independientes: hook (bloquea el comando) → gate G5 (verifica contra el bot vivo) → el propio
código, que RECHAZA abrir posiciones si falta la segunda llave. Solo la tercera es inesquivable.
Y ojo con el modo de fallar: **fail-closed sobre iniciar lo peligroso, nunca sobre supervisar
lo que ya está en vuelo** — [[una-guarda-que-mata-el-proceso-deja-huerfano-lo-que-ya-esta-en-vuelo]].
La auditoría de esa capa destapó además lo peor de todo el día: `uvicorn src.api:app` levantaba la
API sin pasar por `main()`, y `POST /test-order` abría una posición **real** mirando solo si
había claves, sin consultar el modo — la bifurcación paper/live vivía en `place_order`, que
ese camino no usaba. Regla: al añadir una guarda, buscar TODOS los caminos que llegan al
efecto peligroso, no solo el que tienes delante.

**La llave de autorización se ata a lo que autoriza, para que caduque sola.** `LIVE_CONFIRMED`
no vale `1`: tiene que ser igual al nombre de la estrategia que va a operar. Un `=1` en un
panel sobrevive para siempre y deja de significar nada; atarlo al contenido hace que cambiar
la estrategia invalide el permiso.

**Una ronda adversarial no basta.** Contra la guarda de cryptobruj: la 1ª ronda encontró 15
bypasses, se endureció, y la 2ª —contra la versión ya dura, y sin dejarle ver la suite de
tests, que si no audita lo que ya sabes— encontró 7 más y 6 falsos positivos nuevos. Tres de
los agujeros los había introducido yo al endurecer. La regla: al segundo pase se le oculta la
suite, y "todos los casos pasan" solo significa que pasa los casos que se te ocurrieron. Todo
hook de seguridad va con suite de regresión propia; sin ella es otra casilla que se marca a ojo.

Corolario del mismo día: **un comando dentro de una celda markdown no es un gate**
([[un-comando-dentro-de-una-celda-markdown-no-es-un-gate]]). El
escapado de `\|` convirtió la alternancia de un regex en barra literal y dejó el gate de
secretos verde pase lo que pase; `python` a secas no existía en la máquina; y una tubería se
tragaba el exit code del comando de la izquierda, así que el gate pasaba cuando el backtest
reventaba. Los gates van en un `.sh` ejecutable, con exit `2` reservado a "no evaluable" —que
nunca cuenta como verde— y con suite de regresión propia. El `.md` solo describe qué miden.

## LOOP SPEC mínimo

```
GOAL:      <condición objetiva de éxito>
MAKER:     Sonnet (construye) — nunca se autojuzga
CHECKER:   tests deterministas (primario) + browser opcional (secundario) — VETA
STOP WHEN: suite COMPLETA verde + typecheck limpio  OR  <N> iteraciones
ON STOP:   <qué reportar>
```

Sin VERIFY explícito no hay loop, hay agente autoaprobándose.

**Checker determinista primario, no el navegador.** `/fia-verify`/agent-browser es capa SECUNDARIA: es frágil (crashea el renderer, el click no dispara el handler React). Un checker que se cae no verifica, finge. STOP con **suite completa + typecheck**, no solo el test del target: un loop-until-green puede arreglar el objetivo y romper un vecino si el checker solo mira el target (guard anti-regresión).

**Maker ≠ checker:** contexto y modelo distintos; el que hizo el trabajo no es buen juez. **Reparto de modelo por eslabón:** Fable planea · Opus juzga/irreversible · Sonnet construye (maker) · Haiku mecánico/volumen y traer-doc-web (solo fetch).

**Métrica real:** % outputs aceptados sin retrabajo. <50% → el loop cuesta más de lo que ahorra.

**Por complejidad:** prompt inline → `/loop` → `/schedule` → `Workflow` tool (>1 agente o >3 iteraciones). Budget real (contador que corta) solo en `Workflow` (`budget.spent()/remaining()`); en `/loop` a mano = cap de iteraciones + supervisión. No declarar un techo que no mides.

## Loop de ciclo completo

No envuelvo un paso, envuelvo el ciclo: `/loop` que encadena `/prd-to-issues` → `/grill-me` → build → tests+`/fia-verify` → PR → `/fia-cierre`, cada eslabón en su carril de modelo. **Gate "solo sugerencias documentadas":** en el grill auto-acepta una propuesta solo con respaldo real — **Haiku TRAE la fuente, Opus DECIDE si de verdad la respalda** (el juicio de evidencia no va al modelo más débil); sin respaldo → a revisión humana. Maker/checker aplicado a las DECISIONES, no solo al código. No es raíl fijo: los eslabones se combinan según la sesión, el pipeline completo es el máximo no el mínimo. Codificado en el CLAUDE.md global como patrón nombrado para que Claude lo reconozca y lo sugiera.

## El hook que faltaba: no dejar PARAR (3-ago-2026)

Los 5 guards globales eran todos `PreToolUse:Bash` — impiden que Claude **haga** algo malo. Ninguno
impedía que Claude **pare** antes de tiempo, que es lo que hace falta para delegar de verdad: la
autonomía no se compra con permisos, se compra no dejando cerrar el turno hasta que algo determinista
diga que sí.

El `Stop` hook admite `{"decision":"block","reason":"…"}` (equivalente a `exit 2`) y el input trae
`stop_hook_active` para no entrar en bucle. Eso convierte «Claude cree que ha terminado» en «el gate
dice que ha terminado». Los eventos que admiten bloqueo son `PreToolUse`, `PostToolUse`,
`UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact` y varios más; `SessionEnd` y `Notification`
NO (solo efectos secundarios).

Implementado en `~/.claude/hooks/stop-gate.sh` (+ suite propia en `hooks/tests/stop-gate.test.sh`,
20 casos). Decisiones que importan, todas con caso de regresión:

- **Bloquea una sola vez por turno.** Si tras un ciclo sigue rojo, decide el humano, no el bucle.
- **«No evaluable» nunca cuenta como verde** — timeout o comando ausente NO bloquea (infra rota no
  debe secuestrarte el turno) pero **no toca el marcador** y avisa por `additionalContext`. Es la
  misma regla del exit 2 de los gates en `.sh`.
- **Cede ante el hook de proyecto**: si el repo ya tiene su `hooks.Stop`, el genérico se calla. Sin
  esto, en facturaia corrían los dos y bloqueaban por duplicado.
- Detecta código **por extensión, no por directorio** (menos frágil entre Next/Astro/Python/SQL), y
  usa el semáforo `fia-gate` si existe para no saturar la CPU con varias sesiones.
- Escape `CLAUDE_STOP_GATE=off`; no corre en `main`/`master`.

Y el de facturaia, `fia-cierre-reminder.sh`, **pasó de avisar a bloquear**: imprimía un
`systemMessage` y hacía `exit 0` siempre — la casilla marcada a ojo que la propia doctrina condena.

**Corrección el mismo día, y es la lección que queda:** ese hook se colgó primero de cada turno, y
`/fia-cierre` es un gate DE SESIÓN que levanta un Workflow multi-agente (≈12 dimensiones + agent-browser
+ smoke). En una sesión de 8 turnos editando `src/` lo habría pedido 8 veces. Ahora bloquea **una vez
por sesión** (marcador `.git/fia-cierre-sesiones/<session_id>`, escrito ANTES de emitir para que
ignorarlo no lo repita) y elige modo por tamaño del diff (`rapido` con ≤3 archivos).

**La distinción general:** un gate **determinista** (lint/typecheck/tests) cuesta CPU y CERO tokens →
puede correr en cada turno. Un gate **multi-agente** cuesta decenas de agentes → una vez por sesión, o
mejor atado al `git push`, que es cuando el trabajo sale de tu máquina. Enganchar el caro a un evento
de turno es el error caro de este patrón.

**Corolario para el grafo:** el graph engineering NO es la palanca de la autonomía. El grafo reparte
trabajo; lo que te deja irte de casa es el checker determinista. Coherente con «el grafo NUNCA es el
checker».

## Dónde vive cada pieza del harness (jul 2026)

| Pieza | Dónde | Cuándo carga |
|---|---|---|
| Reglas universales | `~/.claude/CLAUDE.md` | siempre (todo proyecto) |
| Reglas por tipo de archivo | `~/.claude/rules/*.md` con `paths:` | solo al tocar archivos que matchean |
| Doctrina de proyecto | `<repo>/CLAUDE.md` | siempre (en ese repo) |
| Rituales ejecutables | `.claude/skills/<x>/SKILL.md` | al invocar `/x` (o auto por description) |
| Enforcement mecánico | hooks en `.claude/settings.json` | en cada tool call (determinista) |
| Conocimiento por disparador | vault `Stack/*.md` | cuando el tema aparece |
| Estado entre sesiones | auto-memory del proyecto | siempre (índice MEMORY.md) |

Regla de reparto: si es un paso a ejecutar → skill; si es prohibición dura → hook (los modelos leen, los hooks bloquean); si es conocimiento condicional → rule con `paths:` o vault; CLAUDE.md solo lo que aplica a TODAS las sesiones.

Las skills soportan contexto dinámico: `` !`comando` `` dentro del SKILL.md se ejecuta al invocar y su output entra en el prompt (ej.: `/agh-start` precarga `git status`, worktrees e issues abiertos). Caso real: harness AGH Ibérica (`/agh-start`, `/agh-pr`, `/agh-end` + hook `git-guard.sh`).

Un `PreToolUse:Bash` puede **reescribir** el comando (no solo bloquear) devolviendo `hookSpecificOutput.updatedInput.command` — base para interceptar de forma transparente. Caso real: [[fia-gate]], semáforo de CPU que enruta `build`/`typecheck`/`lint` por un throttle global cuando hay varias sesiones (soluciona [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] y [[pre-push-build-oom-bajo-sesiones-paralelas]]).

## Skill `dokploy-backup-monitor` — gotchas (caso real Clínica Zen, 2026-07-21)

**Alta en el monitor sin alias SSH previo.** `monitor-onboard.sh` asume que `ssh <alias>` ya funciona (clave o agente). Si el único acceso es una contraseña root: `sshpass -e ssh-copy-id` para autorizar la clave dedicada del portal (`~/.ssh/dokploy_portal_monitor`, se reutiliza el mismo par en todos los servidores), verificar login+`docker stats`, y solo entonces añadir el alias a `~/.ssh/config` para el resto de la skill (fase C usa `ssh <alias>` constantemente).

**`destination.endpoint`/`region` en la BD de Dokploy: no asumas que están bien puestos.** Casos vistos: el operador los metió al revés en la UI, o `region` viene **vacío** (no NULL-como-ausente sino string vacía). Un `read -r EP RG PV` con `IFS=$'\t'` sobre un campo vacío desplaza los valores siguientes. Solución: `COALESCE(NULLIF(col,''),'__EMPTY__')` en el SELECT + comprobar el placeholder tras el `read`, nunca asumir por posición.

**El `appName` que tú escribes en `backup`/`volume_backup` NO es necesariamente la ruta real en S3.** Para BDs dentro de compose, Dokploy sube a `<compose.appName>_<serviceName>/...`, ignorando el `appName` "bonito" que pusiste en la fila. Solo se sabe con certeza dsiparando el backup una vez y mirando `rclone lsl` — no escribas el healthcheck (`PREFIXES`) hasta tener esa confirmación.

**El backup de `web-server` puede reventar el disco si hay stacks con bind-mounts (no volúmenes Docker) de bases de datos vivas** (ej. Supabase con `./volumes/db/data:/var/lib/postgresql/data`). El `rsync -a /etc/dokploy/ ...` de Dokploy copia también esos bind-mounts — WAL de Postgres incluido — a `/tmp`, sobre el mismo disco. Antes de activarlo: `df -h` y `du -sh .../files/volumes/*/data/pg_wal`. Si no cabe, desactivar la fila (`enabled=false`) hasta liberar espacio, no dejarlo fallando cada noche.

**`\d volume_backup` antes de generar el INSERT.** La plantilla asume columnas (`libsqlId`) que no existen en versiones de Dokploy más viejas (v0.28.8 en este caso). Comprobar el esquema real primero evita un ciclo de prueba-error.

**Causa real de disco lleno, ojo antes de asumir "hay que ampliar disco":** revisar `docker system df -v` — un blueprint clonado puede traer un servicio nunca usado por el cliente (aquí: Ollama, 11GB entre imagen+modelo descargado, cero uso real — el chatbot usa OpenAI). Las imágenes `<none>` NO son automáticamente basura: pueden ser la imagen en uso real de un contenedor vivo cuyo tag rotó (Docker lo bloquea solo con "cannot be forced", buena señal de que no hay que tocarlo). Ver [[ollama-blueprint-sin-usar-consume-disco]].

**Si el disco sigue creciendo tras limpiar imágenes/contenedores, mirar el WAL de Postgres antes de ampliar disco.** Un slot de replicación lógica que no avanza (típico: Realtime de Supabase self-hosted en bucle de reconexión roto) retiene WAL sin límite, ignorando `max_wal_size`. Ver [[supabase-selfhosted-realtime-roto-slot-replicacion-crece-wal-sin-limite]].

## `agency-portal` — no tiene API pública para "Añadir servidor" (por diseño)

`createServerAction`/`updateServerAction`/`deleteServerAction` (`src/lib/dokploy/actions.ts`) son **Next.js Server Actions** atadas a la sesión de navegador autenticada (`requireAgencyAccess`), no endpoints REST con API key. El diálogo vive en `src/app/(portal)/agency/infrastructure/server-form-dialog.tsx`. No hay atajo por curl.

Para completar el alta sin pedirle al usuario que pegue el formulario a mano: Playwright con las credenciales reales del portal (`op://Private/Agency-portal-kappa` en 1Password personal, cuenta `my.1password.com`) — login, navegar a `/agency/infrastructure`, `getByLabel()` por cada campo del diálogo (Nombre, Host/IP, Puerto, Usuario SSH, Notas, Clave SSH privada), enviar, y verificar con una captura que la tarjeta aparece con métricas reales. Mismo patrón ya usado para Kommo — reutilizar el perfil persistente de Playwright si ya existe.

**Antes de concluir "esa página no existe en el repo":** comprobar `git log HEAD..origin/main` — el checkout local puede estar en una rama de feature muy atrasada. Leer con `git show origin/main:<path>` sin cambiar de rama (no tocar el checkout de una sesión en curso).

## Rutinas cloud (RemoteTrigger / CCR) — gotchas

Las rutinas de `claude.ai/code` corren en un CCR aislado en la nube de Anthropic (git checkout propio; SIN acceso a tu máquina ni a env locales). Al montar una:
- **Egress allowlist-gated.** Salir a un host privado (p.ej. un Langfuse self-host) da **403 en el CONNECT** por defecto. Fix: editor de la rutina → icono de nube del entorno → engranaje → *Update cloud environment* → **Network access: Custom** + añadir el dominio en **Allowed domains** (marca también "default package managers"). **Se aplica a NUEVAS sesiones** → re-lanzar el run tras guardar. Allowlistar TODOS los hosts que toca: el servicio + `hooks.slack.com` (webhook) + `api.github.com` (`gh`).
- **Identidad de bot:** si adjuntas tu conector MCP personal de Slack, la rutina postea **como tú** (suplantación). Para identidad de bot: **webhook/bot-token** (`curl` a `hooks.slack.com`, requiere allowlist) reusando una app existente (p.ej. "AIA Bot"), y quita el conector personal (`clear_mcp_connections`).
- **El clasificador de auto-mode BLOQUEA `RemoteTrigger create`** de una rutina que egresa PII a la nube si la única autorización vino de un compañero por Slack, no del **propio usuario en sesión** → hace falta el OK directo del dueño de la cuenta.
- **Secretos** van en el prompt de la rutina; las respuestas de la API (`get`/`run`) devuelven el prompt COMPLETO con los secretos → quedan en el transcript, rótalos si importa.
- `RemoteTrigger` (no curl): `list`/`get`/`create`/`update`/`run`. `update` de `job_config` REEMPLAZA el prompt entero (no es patch del texto). No se pueden borrar rutinas por API (UI `claude.ai/code/routines`). Cron en UTC, mínimo 1h.

## Advertencias que pasaron a ser máquina (29-jul)

Las dos reincidieron estando escritas en `hot.md`, así que se automatizaron y **salieron** de
allí por el criterio de salida nuevo ("lo que un hook impide no hace falta recordarlo en
contexto"). Aquí quedan documentadas con su gate:

- **Antes de tocar un ticket, mira si otra sesión ya lo está cerrando** — `gh pr list --state all --search "<área>"`; y al resolver el conflicto quédate las DOS mitades, no elijas lado. Ver [[antes-de-tocar-un-ticket-mira-si-otra-sesion-ya-lo-esta-cerrando]]
  → **Gate**: `~/.claude/hooks/ticket-collision-guard.sh` (UserPromptSubmit). Avisa una vez por sesión de las ramas de worktree con commits sin mergear de las últimas 24 h y **qué ficheros tocan**. Descartadas midiendo dos señales que parecían obvias y no valen: buscar el nº de ticket en GitHub (los PRs del runner lo referencian por UUID) y listar PRs abiertas (11 de 12 eran de dependabot).
- **Una tanda E2E sin comprobar que el servidor sigue vivo al final no es una medición** — `next dev` se murió tres veces a mitad de tanda y sus `ERR_CONNECTION_REFUSED` son indistinguibles de un bug: empujan a subir timeouts. Medir contra `build`+`start`, arrancarlo con `nohup … & disown`, y cerrar con un `curl`. Ver [[tanda-e2e-sin-comprobar-el-servidor-vivo-al-final-no-es-medicion]]
  → **Gate**: `tests/e2e/global-teardown.ts` en facturaia (registrado en `playwright.config.ts`). Al terminar la tanda hace un HEAD a `/login` del `baseURL`; si no responde, marca la tanda **NO CONCLUYENTE** y pone `exitCode = 1` sin reventar el proceso, para no esconder el informe HTML.

## Agentes en paralelo: lo que falla de verdad (3-ago, TuCRMIA)

- **Un agente muere por vigilancia de inactividad y deja la mutación PUESTA.** Los tres agentes de esa
  sesión murieron justo mientras mutaban su implementación para demostrar el rojo: el árbol quedó con
  código deliberadamente roto. Regla: en el prompt, «**restaura antes de informar**»; y el hilo principal
  **revalida siempre** (`typecheck` + suite completa) antes de creerse una entrega. De nueve mutaciones,
  una quedó olvidada — sin revalidar se habría commiteado.
- **Por eso NO un `/loop` de construcción desatendido**: la iteración N+1 hereda lo que rompió la N y su
  gate falla por un motivo que no es el suyo. El loop vale donde cada iteración es pequeña y verificable
  sola (cerrar hallazgos de una lista), no para construir.
- **Techo de tres.** Más agentes no es más trabajo hecho: es más probabilidad de que uno muera a medias.
- **Un fichero, un agente.** Dos sobre el mismo `.sql` de asserts es conflicto garantizado: al segundo se
  le da un fichero aparte y lo fusiona el hilo principal.
- **Ningún agente verifica a otro, ninguno commitea, ninguno corre el gate entero** (tarda y hay trabajo
  concurrente).
- **Sintetizar críticamente**: uno afirmó que un flujo «no se puede completar» cuando en realidad se
  completa **duplicando en silencio**, que es peor. Verificar sus afirmaciones contra el repo.
- **La referencia `fichero:línea` de un agente puede estar INVENTADA aunque su conclusión sea
  correcta** (8-ago-2026, ronda 5 del gate de FacturaIA). El auditor de `datos` citó
  `unidad-material.ts:401-424` y `pedidos-db.ts:266-279`; el fichero tiene 102 líneas y la función
  está en la 52. El fondo era cierto y el veredicto bueno, pero las coordenadas no existían. Lo pilló
  el sintetizador porque **abrió el fichero en vez de creerse la cita** — y eso es lo que hay que
  exigirle al sintetizador, no solo que deduplique. Corolario para uno mismo: al copiar una `ruta:línea`
  de un informe a un commit o a un manual, ábrela; si no, propagas una coordenada falsa con la
  autoridad de un hallazgo verificado.
- **Una dimensión puede caerse o devolver RELLENO, y las dos formas se leen como «revisado»**
  (8-ago-2026, FacturaIA #1550, ronda 4 de `/fia-cierre`). `datos` agotó los cinco reintentos de
  `StructuredOutput` y volvió como `no-ejecutada`; `codigo` devolvió `status: ok`, `summary: "test"` y
  cero hallazgos — sintácticamente válido, sin auditar nada. **Antes de registrar un cierre, contar
  resultados y mirar los `summary`**: un resumen de una palabra o un `findings: []` con `summary` que no
  describe el diff es relleno. Y **registrar por lo que corrió, no por lo que se invocó**: el script se
  llamó con las cuatro y anotarlas habría dejado el árbol diciendo que se miró algo que nadie miró.
  El sintetizador sí lo reportó honestamente (`no-ejecutada` + «el hueco es de bajo riesgo pero no está
  medido») — leer esa nota, no solo el veredicto.

## Medir el coste de un prompt: el recibo, no el proxy (4-ago-2026, AGH #736)

- **La cifra sale del `usage` de la API, nunca de un tokenizador offline.** Contar el JSON de los
  `tools` con `gpt-tokenizer` **sobre-estima ×2,6** lo que cobran: decía **+1.071** tokens por turno y
  el `usage.prompt_tokens` real dio **+415** (+3,0%). La API serializa las definiciones de tools a su
  manera. El conteo offline sigue valiendo para el `SYSTEM_PROMPT` a secas (ahí sí cuadra), no para
  tools.
- **No extrapolar un coste por-unidad medido en otro régimen.** Con UNA tool y un prompt minúsculo,
  `strict` parecía costar +55 tok/tool → «+700 en 14 tools». Medido sobre la superficie real: **+50 en
  total** (+0,36%). El sobrecoste de `strict` es del `required` completo y las uniones nullables, y no
  escala por tool como parecía.
- Corolario de método: **nombra la cantidad exacta que vas a afirmar antes de medirla**, y mídela en la
  misma unidad en que se factura. Las dos correcciones de esa sesión fueron proxies, no errores de
  razonamiento.
