---
title: sandbox-exec filtra la red por puerto y deja abiertos el llavero y los .env
date: 2026-10-17
source: agentesia-skills#37-#40, #42 (plugin pizarra, fuentes.sb)
tags: [macos, sandbox, seguridad, claude-code]
---
Encerrar con `sandbox-exec` (SBPL) un proceso que ha leído contenido no fiable: lo que el perfil `(allow default)` NO cierra solo.

- **Red**: el host de un filtro solo puede ser `*` o `localhost` («host must be * or localhost»). No hay IP, CIDR ni nombre: un puerto abierto lo está hacia cualquier máquina, también la VPN. `localhost` cubre además las IP propias del equipo.
- **Llavero**: `gh` guarda su token ahí y git se lo pide a `gh` → leerlo es poder subir código. Cerrarlo con `(deny mach-lookup (global-name "com.apple.SecurityServer"))`; https sigue funcionando.
- **Credenciales en claro**: `.env*`, `~/.docker`, `~/.npmrc`, `~/.aws`… → `deny file-read-data` (regex `/\.env[^/]*$` + allow de `.example`). Los rodeos por symlink, hardlink o cp quedan bloqueados igual.
- **Copias de la propia herramienta**: Claude Code guarda en claro transcripts (`~/.claude/projects`, `/tmp/claude-<uid>/…/tasks`), `file-history` (cada versión de cada fichero editado, `.env` incluido) y `paste-cache`. Denegar `.env*` sin esto deja una copia de cada uno (#42). Sí dejar `shell-snapshots`/`session-env`: los carga cada Bash.
- **Preferencias**: `defaults write` escribe vía cfprefsd, fuera del encierro → `(deny user-preference-write)`.
- **Apple Events denegados**: `osascript` no falla, se cuelga ~2 min.
- **`mktemp` de macOS** ignora `TMPDIR`: hace falta un shim.
Detalle y tests: README del plugin pizarra en agentesia-skills.
