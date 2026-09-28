---
title: un exit 128 de vault-commit no dice si el push entró
date: 2026-09-28
source: agh-iberica
tags: [vault, git, tooling]
---
`vault-commit --push` devuelve 128 cuando la red corta con `LibreSSL SSL_connect: SSL_ERROR_SYSCALL`. El commit local
siempre queda hecho.
Lo que varía es el push. El 27-sep ese mismo error salió en el fetch posterior y el push SÍ había entrado. El 28-sep
salió en el push y el remoto se quedó en la punta anterior.
El exit code no distingue los dos casos.

Qué hacer: tras cualquier exit ≠ 0, `git log --oneline origin/main..HEAD` + `git ls-remote origin main`.
Si tu commit falta en el remoto, `git push origin HEAD:main` a secas: el commit ya está construido solo con tus rutas.
Nunca repetir `vault-commit`: crearía un segundo commit con el árbol de ese momento, que puede incluir lo ajeno.
