---
title: Codex en Horas IA y cierre Obsidian
date: 2026-09-15
source: agency-portal
tags: [agentesia, codex, horas, obsidian]
---

# Codex en Horas IA

Estado y siguiente acción: [[agentesia]] · [[top-of-mind]].

## Desplegado y verificado

- [PR #644](https://github.com/AgentesIA-MAdrid/agency-portal/pull/644) fusionado y desplegado; merge `74e2ede3a3293fc84be1d8c959ae91cb13937134`. CI verde; lint, tipos, 4891 tests y build superados en checkout limpio de main.
- Migración `20260915180000_codex_member_rate_limits.sql` aplicada; tabla separada de Claude, RLS y permisos verificados. El portal muestra Horas IA y distingue proveedor en sesiones y límites.
- Envío manual de PostToolUse verificado con HTTP 200 y fila de Manu/agency-portal en producción. El último latido comprobado fue manual, a las 15:55:02 UTC; esto no demuestra captura automática.

## Registro automático: pendiente de comprobar

- Instalador: `node ops/codex-time-tracker/install.mjs`. Reutiliza la configuración personal `~/.agentesia-tracker.json`; script instalado en `~/.agentesia/codex-time-hook.mjs`.
- Siete hooks en `~/.codex/hooks.json`: SessionStart, SessionEnd, UserPromptSubmit, PostToolUse, SubagentStop, Stop e Interrupt. Los dos hooks previos de Impeccable se conservaron.
- Se detectaron habilitados pero sin confianza. Tras revisar el script se autorizaron únicamente esos siete hooks; `hooks/list` confirmó todos habilitados y confiables.
- **Manu: cerrar y reabrir Codex, ejecutar trabajo y verificar un latido nuevo en producción y su reflejo en `/agency/time`.** Falta confirmar que la sesión recargue los hooks; no dar por resuelto el síntoma de las gráficas.
- Mejorar instalador/documentación para explicar revisión de confianza y comprobación del primer latido. En otros equipos revisar `/hooks` al instalar.
- PostToolUse limita latidos a uno cada 4 minutos; sesiones con prefijo `codex:`. Resuelve worktrees al repo principal y respeta `.no-tracking`. No recupera horas anteriores ni informa tokens/coste API de Codex.

## Ventana de 5 horas

- `account/rateLimits/read` devolvió para la cuota general `codex` una ventana semanal de 10080 minutos y `secondary: null`. El 5h general queda sin datos; no equivale a 0% ni demuestra ausencia universal de esa ventana.
- Spark (`codex_bengalfox`, GPT-5.3-Codex-Spark) devolvió sus propias ventanas de 300 y 10080 minutos. No sustituir con ellas la cuota general.
- Referencias: [confianza de hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks) · [límites vía App Server](https://learn.chatgpt.com/docs/app-server#6-rate-limits-chatgpt).

## Cierre Obsidian recuperado

- Skill instalada en `~/.codex/skills/obsidian-1/SKILL.md`; invocable como `obsidian1` o `$obsidian-1`. Conserva el original de Claude en `references/claude-original.md`.
- Usa las utilidades locales `~/.claude/bin/vault-*`; guarda resultados y pendientes, protege cambios concurrentes y solicita un OK antes de publicar el vault.
