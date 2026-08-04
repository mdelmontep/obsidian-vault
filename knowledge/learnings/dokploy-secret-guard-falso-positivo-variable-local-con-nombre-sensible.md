---
title: dokploy-secret-guard.sh bloquea Write/Edit por el NOMBRE de la variable local, no por el secreto real
date: 2026-08-04
source: claude-code-session
tags: [claude-code, hooks, harness, secrets]
---

El hook `dokploy-secret-guard.sh` (PreToolUse Write/Edit) bloquea cualquier asignación
`VARNAME = valor` donde `VARNAME` matchea un patrón sensible (`API_KEY`, `TOKEN`, `SECRET`...) case
-insensitive y `valor` no parece placeholder — **aunque el valor sea `os.environ['RETELL_API_KEY']`**,
es decir, código legítimo que lee la clave del entorno, no un secreto en claro.

`RETELL_API_KEY = os.environ['RETELL_API_KEY']` bloquea. `api_key = os.environ[...]` también
bloquea (el regex es case-insensitive sobre el nombre de variable). El único fix es no asignar a
NINGÚN nombre con ese patrón: envolver el acceso en una función (`def auth_header(): return
{'Authorization': 'Bearer ' + os.environ['RETELL_API_KEY']}`) o usar el `os.environ[...]` inline
en el sitio de uso, sin variable intermedia.

Aplica a cualquier script que Write/Edit escriba a disco leyendo credenciales de env — no solo
Dokploy, el hook es harness global.
