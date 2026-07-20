---
title: Claude Code — harness, loops y automatización
date: 2026-07-12
source: CLAUDE.md global (sección "Loops y harness" movida aquí para descargar contexto)
tags: [claude-code, harness, loops, automatizacion]
---

# Harness, loops y automatización

Detalle operativo; el resumen vive en el CLAUDE.md global. Ver también [[claude-code-gotchas]].

## ¿Vale la pena un loop?

Solo si se cumplen los 4:
1. La tarea repite al menos semanal.
2. Algo puede rechazar el output automáticamente (test, lint, build, regla dura).
3. El agente puede cerrarla end-to-end sin devolverte la mitad.
4. "Listo" es objetivo, no de criterio.

Si falta uno → prompt manual.

**Orden de construcción:** manual confiable → skill → loop (con gate) → schedule. Nunca schedulear algo que no probaste a mano.

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

## Rutinas cloud (RemoteTrigger / CCR) — gotchas

Las rutinas de `claude.ai/code` corren en un CCR aislado en la nube de Anthropic (git checkout propio; SIN acceso a tu máquina ni a env locales). Al montar una:
- **Egress allowlist-gated.** Salir a un host privado (p.ej. un Langfuse self-host) da **403 en el CONNECT** por defecto. Fix: editor de la rutina → icono de nube del entorno → engranaje → *Update cloud environment* → **Network access: Custom** + añadir el dominio en **Allowed domains** (marca también "default package managers"). **Se aplica a NUEVAS sesiones** → re-lanzar el run tras guardar. Allowlistar TODOS los hosts que toca: el servicio + `hooks.slack.com` (webhook) + `api.github.com` (`gh`).
- **Identidad de bot:** si adjuntas tu conector MCP personal de Slack, la rutina postea **como tú** (suplantación). Para identidad de bot: **webhook/bot-token** (`curl` a `hooks.slack.com`, requiere allowlist) reusando una app existente (p.ej. "AIA Bot"), y quita el conector personal (`clear_mcp_connections`).
- **El clasificador de auto-mode BLOQUEA `RemoteTrigger create`** de una rutina que egresa PII a la nube si la única autorización vino de un compañero por Slack, no del **propio usuario en sesión** → hace falta el OK directo del dueño de la cuenta.
- **Secretos** van en el prompt de la rutina; las respuestas de la API (`get`/`run`) devuelven el prompt COMPLETO con los secretos → quedan en el transcript, rótalos si importa.
- `RemoteTrigger` (no curl): `list`/`get`/`create`/`update`/`run`. `update` de `job_config` REEMPLAZA el prompt entero (no es patch del texto). No se pueden borrar rutinas por API (UI `claude.ai/code/routines`). Cron en UTC, mínimo 1h.
