---
title: qa visual en git worktree de un proyecto next necesita node_modules y dev (no next start con output standalone)
date: 2026-07-19
updated: 2026-08-06
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

4. **Turbopack NO construye con un `node_modules` symlinkado, esté donde esté.**
   `TurbopackInternalError: Symlink node_modules is invalid, it points out of the
   filesystem root`.
   **CORRECCIÓN 2026-07-30:** esto se atribuyó a cruzar roots de filesystem
   (worktree en `/private/tmp` → `node_modules` en `/Users`). Causa equivocada:
   falla igual con los DOS lados bajo `/Users` (`/Users/x/wt-qa-signo-lineas` →
   `/Users/x/Projects/facturaia/node_modules`), mismo error literal. Mover el
   worktree a `/Users` no arregla nada; el symlink ES el problema → hardlinks o
   clonefile (puntos de abajo).
   Lo caro: `vitest` y `tsc` SÍ resuelven el symlink. Un agente puede entregarte
   8.500 tests y typecheck verdes en un worktree que no compila.
   **El `pre-push` lo canta como «Push bloqueado: build con errores»** (06-ago, dos
   veces en la misma sesión), que se lee como defecto del diff cuando es el entorno.
   Si lo que empujas no toca código de la app —dos JSON de baseline y un `.md`—,
   sospechar del `node_modules` antes que del cambio.

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

5. **⚠️ El symlink puede apuntar a un `node_modules` YA CADUCO — y engaña al preflight**
   (06-ago-2026). El del checkout principal se queda atrás en cuanto una PR ajena añade una
   dependencia: en agh-iberica le faltaba `playwright` desde hacía días, así que `npm run gate`
   salía ROJO ahí sobre `main` limpio, y parecía un fallo de código. Al symlinkar un worktree
   nuevo a ese árbol, el fallo se hereda.
   Un preflight que comprueba que `node_modules` **exista** (no que esté al día) lo da por
   bueno: el symlink lo satisface trivialmente. Regla: en un worktree que vaya a correr el
   gate, `npm ci` de verdad — el symlink solo para inspección rápida. Y al ver un rojo,
   descartarlo primero contra `main` antes de sospechar del diff.

