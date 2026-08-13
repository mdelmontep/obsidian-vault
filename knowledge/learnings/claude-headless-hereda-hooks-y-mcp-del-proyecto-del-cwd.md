---
title: claude -p headless hereda hooks y mcp del proyecto del cwd
date: 2026-08-13
source: claude-code-session
tags: [claude-code, headless, runner]
---
Un `claude -p` lanzado por un runner/script carga el `.claude/` del directorio
actual: hooks de SessionStart, MCP servers del `.mcp.json`, CLAUDE.md. Probado
desde un checkout de facturaia: el mismo prompt que en un dir vacío responde en
2 s, dentro del repo se quedó colgado >3 min cargando MCPs, y con `--max-turns 1`
devolvió `is_error` (los hooks consumen el turno).

Fix doble para cualquier ejecutor headless (runner de contenido, contenido-07):
1. `cwd` NEUTRO explícito en el spawn — `mkdtempSync(join(tmpdir(), ...))` — aunque
   el contenedor ya tenga WORKDIR limpio: en local te salva.
2. stdin CERRADO (`promesa.child.stdin.end()` con execFile): el CLI espera datos
   3 s y puede fallar con «no stdin data received» si el pipe queda abierto.
