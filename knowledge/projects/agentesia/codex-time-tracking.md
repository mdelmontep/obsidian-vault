---
title: Codex en Horas IA y cierre Obsidian
date: 2026-09-15
updated: 2026-09-15
source: agency-portal
tags: [agentesia, codex, horas, obsidian]
---

# Codex en Horas IA

Contexto: [[agentesia]] · [[top-of-mind]].

## Desplegado

- [PR #644](https://github.com/AgentesIA-MAdrid/agency-portal/pull/644) fusionado y desplegado (`74e2ede3`); migración `20260915180000_codex_member_rate_limits.sql` aplicada y permisos verificados. Límites de Claude y Codex en tablas separadas.
- [PR #645](https://github.com/AgentesIA-MAdrid/agency-portal/pull/645) (`d1502122`) estabiliza la ruta de Node del instalador para conservar la confianza, evita reescribir `hooks.json` sin cambios, reduce PostToolUse de 4 a 1 minuto y hace visibles minutos cortos en las barras.
- [PR #646](https://github.com/AgentesIA-MAdrid/agency-portal/pull/646) (`49f6a708`) añade un selector al gráfico por proyecto: permite leer `agency-portal` aunque en la vista agregada quede dentro de «Otros». Ambas PR fusionadas y desplegadas; lint, tipos, pruebas y build locales pasaron. Actions no inició CI por facturación de la cuenta, no por fallo de código.

## Captura automática: comprobada en producción

- Instalador: `node ops/codex-time-tracker/install.mjs`; script `~/.agentesia/codex-time-hook.mjs`, configuración personal `~/.agentesia-tracker.json`. Los 7 hooks de Codex en `~/.codex/hooks.json` siguen `enabled` + `trusted` según `hooks/list`; los 2 de Impeccable se conservaron. En otros equipos hay que revisar y confiar sus comandos.
- La sesión real `codex:01a0a5f6-1325-7433-8249-68253b15684d` envió latidos automáticos separados por más de 60 s; `last_activity_at` avanzó en PostgreSQL hasta 17:55:12 UTC. El HTTP 200 manual de 15:55:02 UTC fue solo diagnóstico inicial.
- Prueba nueva `codex:01a0a63d-2e7e-7442-b6c9-aebc6ff79fe2`: 2 prompts, 2 llamadas `exec` separadas por 60 s; bloque automático Manu/agency-portal de 18:03:53 a 18:05:04 UTC (71 s), `prompt_count=2` y último `Stop` persistidos.
- Manu vio en el gráfico por técnico un tooltip de 23 min a las 19:00 antes del backfill. Tras el despliegue y la incorporación del histórico confirmó visualmente correctos ambos gráficos. La consulta de duración para «Hoy» a las 18:17 UTC daba Manu ≈12h 32m y `agency-portal` ≈4h 37m; son cifras del día completo y cambian con sesiones activas.

## Histórico previo a la conexión (15-sep)

- Manu eligió reconstruir los tres proyectos según el `cwd` de los rollouts Codex. Ventana: 16:00–18:46 de Madrid, hasta el primer registro automático; el primer evento local de Codex es hacia las 16:51. El trabajo previo de Claude Code ya tenía filas y no se inventó una franja continua.
- Desde los pares `task_started`/`task_complete` y llamadas de herramienta se insertaron transaccionalmente 36 bloques cerrados: `agency-portal` 7, `agh-iberica` 6 y `facturaia` 23. Fuente `backfill-codex-jsonl`, prefijo `codex:` y guardia contra duplicados; segunda pasada dry run: 0 pendientes. Las 5 filas existentes del tramo se respaldaron antes y no se modificaron.
- En esa ventana, el tiempo fusionado por técnico pasó de 47 a **158 min**. Por proyecto, después del backfill: `agency-portal` **61 min**, `agh-iberica` **153 min** (incluye 46 min de Claude Code ya registrados) y `facturaia` **90 min**. Sesiones paralelas se fusionan para Manu; cada proyecto conserva su propio intervalo. No se añadieron tokens/costes ni se alteraron cuotas.

## Ventana de 5 horas

- `account/rateLimits/read` devolvió para la cuota general `codex` una ventana semanal de 10080 minutos y `secondary: null`. El 5h general queda sin datos; no equivale a 0% ni demuestra ausencia universal de esa ventana.
- Spark (`codex_bengalfox`, GPT-5.3-Codex-Spark) devolvió sus propias ventanas de 300 y 10080 minutos. No sustituir con ellas la cuota general.
- Referencias: [confianza de hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks) · [límites vía App Server](https://learn.chatgpt.com/docs/app-server#6-rate-limits-chatgpt).

## Cierre Obsidian recuperado

- Skill instalada en `~/.codex/skills/obsidian-1/SKILL.md`; invocable como `obsidian1` o `$obsidian-1`. Conserva el original de Claude en `references/claude-original.md`.
- Usa las utilidades locales `~/.claude/bin/vault-*`; guarda resultados y pendientes, protege cambios concurrentes y solicita un OK antes de publicar el vault.
