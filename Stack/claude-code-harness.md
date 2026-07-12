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
GOAL: <condición objetiva de éxito>
VERIFY: <qué lo falla automáticamente>
STOP WHEN: éxito OR <N> iteraciones
ON STOP: <qué reportar>
```

Sin VERIFY explícito no hay loop, hay agente autoaprobándose.

**Maker/Checker:** agente rápido/barato que produce + agente lento/estricto con instrucciones distintas que verifica. El que hizo el trabajo no es buen juez.

**Métrica real:** % outputs aceptados sin retrabajo. <50% → el loop cuesta más de lo que ahorra.

**Por complejidad:** prompt inline → `/loop` → `/schedule` → `Workflow` tool (>1 agente o >3 iteraciones).

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
