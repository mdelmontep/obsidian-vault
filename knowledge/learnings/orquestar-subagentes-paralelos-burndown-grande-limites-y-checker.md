---
title: orquestar subagentes paralelos para un burndown grande — límites y checker real
date: 2026-07-16
source: claude-code-session
tags: [claude-code, subagentes, harness, orquestacion]
---
Barrido masivo (cientos de sitios, ~170 ficheros) repartido en agentes por carpeta disjunta, gateados por un lint. Aprendido a base de romperlo:

- **Máx 2-3 agentes concurrentes.** 5 a la vez tumbaron la sesión por session-limit (mueren a media edición → árbol parcial/roto). Fan-out amplio = fragilidad. Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]].
- **Los agentes NO deben tocar estado COMPARTIDO**: `npm run build` (corrompe el `.next` común bajo paralelismo), `git stash`/`checkout`/`reset` (un subagente hizo `git stash` que revirtió el `eslint.config` estricto sin commitear y barrió fixes a un stash → eslint pasaba en falso), ni el propio `eslint.config`. El orquestador es dueño de config/git; los agentes solo editan SUS ficheros.
- **El orquestador es el checker REAL, no te fíes del auto-verify del agente.** 2ª confirmación (burndown 42703, 9 agentes): el `tsc --noEmit` COMPLETO del orquestador cazó **4+ bugs reales que el `eslint`-scoped de los agentes NO ve** (`GenericStringError`/`ParserError` de embeds/selects dinámicos, implicit-any tras quitar cast sobre cliente `any`). El eslint gatea la SINTAXIS del cast; solo el tsc completo valida el TIPO resultante. Tras CADA lote: `tsc --noEmit` COMPLETO + tests + grep del diff por red flags (`as any`/`@ts-ignore`/`: any`/`as unknown as`). Da a los agentes `eslint scoped` como gate y **prohíbeles lanzar comandos en background** (dejaban `tsc`/waiters colgados que re-notificaban en bucle; matar el loop padre `until [ -s …output ]`, no solo el `sleep`).
- **Commit por zona** (folder-scoped: amplía el scope del gate al completar cada zona) → progreso commiteable e independiente; un agente que muere no tira lo ya commiteado. Un push al final (build del hook ~7min). Ver [[refactor-ui-grande-agentes-paralelos-particionados-por-archivo]] · [[supabase-subagent-driven-development-paralelo-requiere-commits-y-archivos-exclusivos]].
