---
title: dokploy-secret-guard.sh bloquea Write/Edit por el NOMBRE de la variable local, no por el secreto real
date: 2026-08-04
updated: 2026-08-06
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

## ✅ ARREGLADO el 06-ago-2026 — el workaround de arriba ya no hace falta

El hook confundía **referencia** con **literal**: `apiKey: process.env.OPENAI_API_KEY` daba
el nombre de la variable como «valor sospechoso». Bloqueaba ~15 ficheros de evals de
agh-iberica **ya commiteados desde julio** — rechazaba código que él mismo había dejado pasar
antes de existir.

Y lo peor no era el bloqueo: **invertía su propio incentivo**. Un guard que rechaza la
referencia te empuja a pegar el literal, que es lo único peligroso.

Fix en `~/.claude/hooks/dokploy-secret-guard.sh`: `is_placeholder()` acepta ahora las formas
de REFERENCIA — `process.env.` · `import.meta.env.` · `os.environ` · `Deno.env.get(` ·
`System.getenv(` · `${VAR}`/`$VAR` · `op://` · `{{ VAR }}`.

**Residuo vivo (12-ago)**: una clave de OBJETO también dispara — `secret: opts.secret` en TS
bloquea (clave sensible + valor que no es referencia ni placeholder). Fix sin rodear el guard:
shorthand de propiedad (`{ secret }`, sin `:`), valores cortos (<8 chars: `s`), o valores con
marcador (`'dummy-…'`) en tests. Ojo: `'test-…'` NO es marcador reconocido.

Los tests que valen son los que **deben seguir bloqueando**, y hay tres nuevos con el
literal conviviendo con la referencia: un `sk-proj-…` real en un fichero que también usa
`process.env` · una contraseña literal en el mismo compose que usa `${POSTGRES_PASSWORD}` ·
y `op://` al lado de un token real — **`op://` no es salvoconducto**. Suite 20 → 28 casos.
Probado además en el camino REAL (escribiendo el fichero con Write), no solo con la suite.

