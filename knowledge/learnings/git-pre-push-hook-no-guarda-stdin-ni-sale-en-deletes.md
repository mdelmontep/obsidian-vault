---
title: pre-push hook corre build incluso en git push --delete si no guarda stdin
date: 2026-06-19
source: claude-code-session
tags: [git, hooks, ci]
---

`git pre-push` recibe los refs por stdin: `<local_ref> <local_sha> <remote_ref> <remote_sha>`.
En un delete, el SHA local es `0000000000000000000000000000000000000000`.

Si el hook no lee stdin al inicio, un `npm run build` bloqueante antes del check bloquea
todos los `git push --delete`, impidiendo limpiar ramas mergeadas.

Fix: guardar stdin al inicio y salir si todos los refs son deletes:

```bash
stdin_data=$(cat)
non_delete=$(echo "$stdin_data" | awk '{print $2}' | grep -v '^0\{40\}$' || true)
if [ -z "$non_delete" ]; then exit 0; fi
```

Caso real 2026-06-19: limpieza de 60+ ramas mergeadas bloqueada por build en pre-push.
