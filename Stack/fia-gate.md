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
- Matchear el comando por POSICIÓN, no substring → [[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]].
- Banner UI a medida desde script no es fiable → [[ui-flotante-desde-script-macos-swiftdialog-no-osascript-panel]].
- BSD sed / while-read → [[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]].
