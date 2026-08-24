---
title: un push que se cae por red imprime «Everything up-to-date» al final y la rama no existe en el remoto
date: 2026-08-20
source: facturaia
tags: [git, verificacion, arnes]
---
Un `git push` cortado por red deja una salida que **acaba en una línea de éxito**:

    error: RPC failed; curl 35 Send failure: Broken pipe
    send-pack: unexpected disconnect while reading sideband packet
    fatal: the remote end hung up unexpectedly
    Everything up-to-date          ← esto es lo último que se lee

Leer solo el final (o un `| tail`) da por subido algo que no existe en el remoto. El exit code sí es 1, pero si el push va dentro de un wrapper que hace `echo` después, el exit del wrapper tapa el del push.

- **La verificación que decide no es el exit code, es la punta**: `git ls-remote origin <rama>` == `git rev-parse HEAD`. Aplica **también cuando el push dice que fue bien**, no solo tras un pipe.
- El riesgo se multiplica con hooks `pre-push` lentos (lint+typecheck+build): el push tarda minutos, se lanza en background y la salida se mira de refilón.
- Y `git ls-remote` **también** puede fallar por red (`SSL_ERROR_SYSCALL`) devolviendo vacío: un remoto vacío puede ser «no existe» o «no pude preguntar». Reintentar antes de concluir.
- **Tercer significado del vacío, encontrado el 24-ago: la rama ya BORRADA.** Tras `gh pr merge
  --delete-branch`, un `ls-remote` de esa rama sale vacío con exit 0 — y leerlo como «nunca
  estuvo» es tan falso como leerlo como «no existe». Las tres lecturas del vacío (ausencia,
  error, borrado) solo se distinguen sabiendo **qué ha pasado en medio**. Ese día las dos
  sesiones cometieron una cada una, en direcciones opuestas.

- Reincidencia el 22-ago con el wrapper que la propia nota predecía: `git push > log 2>&1; echo "exit=$?"`
  lanzado en segundo plano. El aviso del arnés dijo **«completed (exit code 0)»** — ese 0 es del
  wrapper, no del push, y el `echo` fue a un stdout que no se capturó. El remoto siguió en la punta
  vieja. Lo cazó comparar SHAs, no leer el exit.

Mismo patrón que [[push-por-pipe-oculta-el-abort-del-pre-push-y-el-merge-squashea-punta-vieja]] pero con otra causa: ahí la culpa era del pipe, aquí de una línea de éxito impresa después del fallo.

Relacionado: [[facturaia]]
