---
title: qa visual en git worktree de un proyecto next necesita node_modules y dev (no next start con output standalone)
date: 2026-07-19
source: claude-code-session
tags: [git-worktree, nextjs, qa, playwright]
---
Para QA visual en paralelo se crea un `git worktree` desde `origin/main`, pero:

1. El worktree NO trae `node_modules` (git no lo versiona). Sin él, `npx vitest`
   coge un binario ajeno y falla (`Cannot find module 'vitest/config'`).
   Fix: `ln -s <checkout-principal>/node_modules node_modules` en el worktree
   (misma base reciente + mismo arch → seguro). Lo mismo para `.env.local`/`.env.test`
   (gitignored): copiarlos del checkout principal.
2. `next start` NO funciona con `output: 'standalone'` (avisa y sale). Para QA usar
   `npm run dev` (Turbopack) en un puerto propio (`PORT=3013`), no `next start`.
3. Playwright: un `getByText('Calendario')` puede coger a la vez el enlace del menú
   lateral (`<a>`) y el toggle de vista (`<button>`) → navega fuera. Scopear por tag:
   `locator('button').filter({hasText:/^Calendario$/})`.

4. Si el gate pre-push (o cualquier `next build` con Turbopack) va a correr en el
   worktree, este DEBE vivir bajo el MISMO root de filesystem que el `node_modules`
   real. Un worktree en `/private/tmp/...` con symlink a `/Users/.../node_modules`
   revienta: `TurbopackInternalError: Symlink node_modules is invalid, it points
   out of the filesystem root`. Fix: crear el worktree en `/Users/...` (p. ej.
   `/Users/<user>/<repo>-fb`), no en el scratchpad de `/tmp`. Caso real 2026-07-20:
   push de PR bloqueado hasta mover el worktree de `/private/tmp` a `/Users`.

   **Mejor alternativa (2026-07-25): `cp -al <principal>/node_modules <worktree>/node_modules`.**
   Hardlinks en vez de symlink: instantáneo (segundos, no los ~2 min de `npm ci`), sin duplicar
   1,3 GB reales, y Turbopack ve ficheros de verdad, así que funciona **también desde `/tmp`**.
   Limitación: solo para leer (lint/typecheck/build). Si vas a correr `npm install`/`npm ci` en el
   worktree, NO uses hardlinks — comparten inodo con el checkout principal. Ahí toca `npm ci` propio.
   Al limpiar, `rm -rf node_modules` en el worktree ANTES de `git worktree remove`; verificado que el
   contador de ficheros del principal no cambia (borrar un hardlink solo baja el nº de enlaces).

5. **Monorepo con sub-app (2026-07-27, agh-iberica):** el worktree tampoco trae el `node_modules`
   de la sub-app (`dashboard/`), que es un install aparte → el gate raíz sale **rojo con 9 ficheros**
   por `Cannot find package 'react-dom/server'` y parece un fallo del diff. Es ENTORNO: enlazar
   también `dashboard/node_modules` del checkout principal. Con vitest el symlink basta (el veto de
   Turbopack del punto 4 no aplica). Comprobar el `.gitignore`: si `node_modules` está SIN barra,
   el symlink queda ignorado y no se cuela en el commit.

Cuándo aplica esto: el checkout principal lo van cambiando de rama sesiones
paralelas y su `.next` lo corrompen builds concurrentes → aislar commit+push en
worktree propio (ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]).

Limpieza al acabar: `rm node_modules` (symlink) antes de `git worktree remove --force`.
Ver [[facturaia]].

6. **Si vas a correr `npm install`/`npm ci` en el worktree (2026-07-27):** ni symlink ni
   hardlinks. En APFS, `cp -Rc <principal>/node_modules <worktree>/node_modules` hace un
   **clon copy-on-write**: ~16 s para 1,3 GB, sin ocupar disco real hasta que algo cambia, y
   son ficheros de verdad (Turbopack contento, y `npm ci` puede reescribir sin tocar el
   checkout principal). Es la opción segura cuando el worktree va a mutar dependencias, como
   al probar un bump de Dependabot.

