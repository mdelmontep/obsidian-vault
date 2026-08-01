---
title: una tanda E2E con los specs de una rama y el binario de otra no mide nada
date: 2026-08-01
source: claude-code-session
tags: [e2e, testing, playwright, git, worktree]
---
Lancé la suite desde el repo raíz (en `main`, con el spec viejo) contra un servidor construido con
el código de la rama: **6 fallos**. Repetida desde el worktree de la rama, con sus specs y su
binario: **1**. Los otros 5 eran la mezcla de versiones, y uno de ellos (`modulo-config-autosave`)
me tuvo un rato buscando una regresión que no existía.

Playwright coge los specs del `cwd`; el servidor sirve el `.next` de donde se construyó. Con
worktrees esos dos sitios se separan sin avisar y el marcador sigue saliendo, con pinta de válido.

Reglas:
- Correr la suite SIEMPRE desde el mismo checkout que construyó el servidor. Comprobarlo, no
  suponerlo: `git -C <dir> log -1 -- <ruta-del-spec>` en los dos lados.
- Un rojo se clasifica construyendo `origin/main` **en el mismo worktree**, con el mismo servidor y
  los mismos datos. Si falla igual, es preexistente; ahí se acaba la discusión.
- Contención ≠ preexistente ≠ regresión: lo aislado descarta contención, lo de `main` descarta
  regresión.

**Ampliación 1-ago: el servidor miente de tres formas más, y me pasaron las tres el mismo día.**
Cinco mediciones inválidas seguidas, y en las cinco concluí «esto no funciona» sobre algo que sí
funcionaba:
1. **Reconstruí con el servidor vivo.** `npm run build` sustituye el `.next` por debajo; el proceso
   sigue con el manifiesto viejo y pide chunks que ya no existen. Da 500 en consola, no en la
   pantalla, y la página se degrada en silencio.
2. **El servidor nuevo no arrancó.** `EADDRINUSE`, porque mi `pkill` no casaba con el proceso real,
   y seguí midiendo el viejo sin enterarme. `npm run start` no falla de forma visible si lo lanzas
   en segundo plano.
3. **Un `node .next/standalone/server.js` sin entorno.** Arranca y responde 200 en `/login`, pero
   revienta en cuanto necesita la BD (`supabaseKey is required`), así que la página sale vacía y
   parece un bug de producto.

El chequeo que las caza todas, y cuesta dos líneas: **comparar el `BUILD_ID` que sirve el proceso
con el del disco ANTES de medir**. `curl -s $URL/login | grep -F -e "$(cat .next/BUILD_ID)"`. Si no
coincide, no hay medición. (Ojo: el `BUILD_ID` puede empezar por guion y `grep` lo tomaría por una
opción; de ahí el `-F -e`.)

Y una cuarta forma de mentirte a ti mismo sin tocar el servidor: **buscar en la pantalla un texto
que no existe**. Di por hecho el copy del upsell (`no está incluido`) cuando decía `no están en tu
plan`, y anoté «la UI no gatea». Antes de concluir por ausencia, saca la aguja del código.

Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] ·
[[un-checker-que-se-pone-rojo-por-la-razon-equivocada-es-peor-que-no-tenerlo]]
