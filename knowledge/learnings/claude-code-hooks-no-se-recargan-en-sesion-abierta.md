---
title: instalar/actualizar hooks de Claude Code no afecta a una sesión ya abierta
date: 2026-07-22
source: claude-code-session
tags: [claude-code, hooks, gotcha]
metadata:
  type: learning
---

`~/.claude/settings.json` (hooks) se lee al ARRANCAR la sesión de Claude Code, no en caliente. Si corres un `install.sh` que registra/actualiza un hook (o cambias el propio script del hook) mientras ya tienes una sesión abierta, esa sesión sigue sin dispararlo — hace falta cerrarla y abrir una nueva.

Síntoma real: reinstalar el tracker de `ops/claude-time-tracker` y seguir escribiendo en una sesión que ya estaba abierta antes del reinstall → cero eventos nuevos, parece que el hook está roto cuando en realidad nunca se cargó para esa sesión.

**Checklist de diagnóstico cuando "el hook no hace nada" tras instalar/actualizar**:
1. ¿Es una sesión NUEVA (abierta después del install)? Si no, esa es la causa más probable — cerrar y reabrir antes de seguir investigando.
2. Config existe y con los valores correctos (`~/.agentesia-tracker.json` o equivalente).
3. El hook está registrado en `~/.claude/settings.json` (grep del comando).
4. Test manual: invocar el endpoint/comando directamente (sin pasar por el hook) para descartar problema de red/servidor vs. problema de disparo del hook.
