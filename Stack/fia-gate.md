---
title: fia-gate — semáforo de CPU entre sesiones Claude
date: 2026-07-17
source: claude-code-session
tags: [claude-code, harness, cpu, worktree, macos]
---

# fia-gate

Semáforo de CPU global (en disco) que evita que varias sesiones/worktrees de Claude Code saturen la máquina corriendo `build`/`typecheck`/`lint` a la vez. Es la solución automatizada a los pains manuales de [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] y [[pre-push-build-oom-bajo-sesiones-paralelas]] ("espera a la ventana libre").

Vive en `~/.claude/gate/` (impl completa en la memoria del agente, no duplicar aquí). Montado 2026-07-17.

## Cómo funciona
- **Hook** `~/.claude/hooks/gate-hook.sh` (`PreToolUse:Bash` en `~/.claude/settings.json`) intercepta los comandos pesados y los **reescribe** vía `hookSpecificOutput.updatedInput.command` para pasarlos por `~/.claude/gate/fia-gate` (base64). Transparente: Claude no escribe nada especial. **Solo se activa en sesiones ARRANCADAS tras añadir el hook** (se carga al inicio; reiniciar las abiertas).
- **Admisión adaptativa por carga** (no N fijo): corren libres hasta MIN (suelo), crecen solo si `loadavg1 < cores×factor`, con MAX como techo duro. Config global en `~/.claude/gate/state/{slots,max,loadmax}.conf` (def MIN 2 / MAX 5 / factor 0.85). Admisión **atómica** con mutex mkdir por PID (si no, arranques simultáneos se saltan el límite, TOCTOU).
- **Badge** SwiftBar (barra de menú): fase en vivo, `corriendo/MAX`, carga+⚠ al saturar, cancelar por job. Dashboard TUI: `node ~/.claude/gate/gate-dash`.

## Gotchas que salieron (learnings)
- **`git commit` no pasa por el hook, y el `pre-commit` corre `npm run gate` entero FUERA del semáforo** (3-sep): el hook solo envuelve `npm run gate/test/build/lint/typecheck`, `vitest`, `tsc --noEmit` y `git push` en posición de comando. Para respetar los slots: `FIA_GATE_KIND=mem "$HOME"/.claude/gate/fia-gate --b64 <base64 de "cd wt && git commit -F msg > log 2>&1">`. Con otras sesiones ocupando los slots, cada intento espera 40-60 min: dejar TODO listo antes (baselines, cifras, tablero), y recordar que `mutate-guard` solo recuerda víctimas de las últimas 2 h.
- **Un lanzador `nohup zsh -c "git commit …; git push …"` también entra en la cola, y relanzarlo lo duplica** (3-sep): el hook lo manda a background al pasar 120 s; si crees que no salió y lo vuelves a lanzar, la cola ejecuta los dos —dos `amend` y dos push a la vez, y el waiter casa con el log viejo. Un solo lanzador por intento, esperar su notificación, y solo entonces el waiter sobre el log.
- **Un `pgrep -f "npm run gate|…"` también se envuelve**: el hook trocea por `|` y ve `npm run gate` en posición de comando → un `ls` inocente se queda en cola detrás de un build. Palabras vigiladas fuera de los comandos de consulta.
- **El watchdog mataba la cadena entera con un solo presupuesto de 900 s** (`is_simple_chain` no trocea si hay `;`/`|`/comillas) → [[fia-gate-watchdog-mata-la-cadena-entera-con-un-solo-presupuesto]]. **Arreglado 29-jul**: `count_heavy()` escala el presupuesto al nº de comandos pesados del segmento y el watchdog avisa por stderr al matar (antes solo `rc=143` mudo). Verificado A/B con `FIA_GATE_TIMEOUT=60`: n=1 muere a los 60 s, n=2 sobrevive.
- **Diagnosticar muertes con `state/events.jsonl`, no por hipótesis**: la secuencia `queued/running/phase/timeout/done` + `rc` dice quién mató el job. Sin evento `done` = lo mató el harness, no el gate.
- Matchear el comando por POSICIÓN, no substring → [[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]].
- Banner UI a medida desde script no es fiable → [[ui-flotante-desde-script-macos-swiftdialog-no-osascript-panel]].
- BSD sed / while-read → [[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]].
- **Un push encolado sube el HEAD de cuando sale, no el de cuando se lanzó**: no commitear mientras espera → [[un-push-encolado-en-fia-gate-empuja-el-head-del-momento-en-que-sale]].
- **El `pre-push` envuelto REENTRA: no pide slot y no escribe ningún evento** (23-sep, `fia-gate:116-121`): si el comando padre ya tiene slot, los descendientes heredan `FIA_GATE_HELD` y la invocación anidada corre `bash -c "$CMD"; exit $?` sin pasar por admisión ni por `logev`. Es deliberado —sin esa puerta el hook pediría un slot `mem` que su padre ya tiene, el interbloqueo del 24-ago—, pero tiene dos consecuencias que cuestan trabajo: **propagar el `session` real de Claude Code a los procesos `githook-*` NO sirve de nada** (el hook nunca lee la variable; abrí el PR #2891 para eso y lo cerré sin mergear tras medirlo: su propio push quedó como UNA invocación de 18m42s sin etapas intermedias), y el ahorro del segundo slot `mem` es **bimodal por esto, no por ruido** — push envuelto espera 0, push suelto pide un slot por etapa. Promediar las dos poblaciones mezcla cosas distintas.
- **El gate SÍ propaga el exit code** (`run_seg` → `RC=$?` → `exit $RC`, líneas 412/437/439): si ves un 0 donde esperabas un rojo, mira tu propia cadena antes de acusarlo — `cmd > log 2>&1; ec=$?; echo "ec=$ec"` devuelve el 0 del `echo`. Hermano de «ningún gate por pipe». Y desde el 23-sep `state/events.jsonl` **se archiva antes de truncar** (`state/archive/events-AAAAMMDD.jsonl.gz`, fail-closed, prueba en `~/.claude/hooks/tests/fia-gate-retencion.test.sh`): antes rotaba a 500 líneas al pasar de 2 MB y tiraba el resto, así que no había histórico con el que pesar nada. Ver [[una-lectura-de-load1-no-acredita-una-ventana-de-medida]] · [[un-ensayo-en-seco-que-sustituye-el-gate-no-prueba-la-medida]].
