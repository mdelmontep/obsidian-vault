---
title: matar el git push deja el pre-push huérfano, y ese retiene el candado compartido sin empujar nada
date: 2026-09-28
source: facturaia
tags: [git, hooks, fia-dbtest, coordinacion-sesiones]
---
- `pkill -f "git push …"` mata a git, pero `bash .githooks/pre-push` sigue vivo con ppid 1 y termina su cadena entera.
- Ese huérfano esperó el candado `/tmp/fia-dbtest.lock`, lo cogió en cuanto otra sesión lo soltó y corrió la integración. Tapó el turno pactado con otra sesión y no iba a empujar nada: su padre estaba muerto.
- Para cortar un push, mata el ÁRBOL del hook (`pkill -f "pre-push origin"` y sus `vitest`/`test-integracion`). Verifícalo con `ps` y con `cat /tmp/fia-dbtest.lock/owner`, no con el exit code del push (sale 144 y parece cortado).
- Corolario: el pre-push ya hace cola con `mkdir` atómico, así que el push se puede lanzar sin esperar el LIBERO. Lint, typecheck y suite avanzan y la integración entra cuando le toca.
- Caso: #3051, 28-sep-2026. Relacionado: [[hooks-lentos-repo-compartido-usar-background-y-poll]].
