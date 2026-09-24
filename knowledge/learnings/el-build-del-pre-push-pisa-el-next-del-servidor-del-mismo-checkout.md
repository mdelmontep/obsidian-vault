---
title: el build del pre-push pisa el .next del servidor que corre en el mismo checkout
date: 2026-09-24
source: facturaia
tags: [pre-push, next, e2e, worktree, staging]
---
Si el pre-push hace `next build` y a la vez un servidor (staging, dev) sirve desde el MISMO checkout, el build reescribe `.next` debajo del servidor vivo. Además lo compila con el `.env.local` de ese árbol, que puede ser el de PRODUCCIÓN.

Síntoma: la etapa E2E que va después (candado de permisos) no encuentra ni `#login-email`. Parece un fallo de login o de datos, y es el servidor sirviendo un bundle a medio escribir.

Fix: el servidor contra el que corre el E2E vive en un worktree aparte, del mismo commit (`git worktree add --detach`, `node_modules` clonado con `cp -Rc`, nunca symlink), y en su propio puerto. Si el guard «el servidor no es de este árbol» salta, la salida documentada es `E2E_PERMITIR_SERVIDOR_AJENO=1`, que es legítima solo si el otro árbol está en el mismo commit.

Caso: facturaia ticket 183 (24-sep-2026). El push 4 cayó en el candado y el 7 pasó entero con el staging en `fia-183-staging:3008`.

Alternativa sin worktree extra (facturaia #2930, mismo día): el staging en modo `next dev` (`PORT=3019 scripts/dev-staging.sh`, sin `build`) y `E2E_BASE_URL=http://localhost:3019 git push`. El dev no toca el `.next` del build, así que ni lo pisa el pre-push ni invalida su caché de build; `dev-staging.sh build` sí la invalida y el push vuelve a compilar y a romperlo, en bucle.
