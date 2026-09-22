---
title: npx --no-install no busca en el PATH, busca en el bin del prefijo global de npm
date: 2026-09-22
source: facturaia
tags: [npm, npx, node, ci, supabase]
---

`npx --no-install <cli>` resuelve en `node_modules/.bin` y en el bin del **prefijo global de npm**;
si no está en ninguno, aborta con `npx canceled due to missing packages`, aunque `which <cli>` lo
encuentre en el PATH.

Caso (22-sep, Mac de CI): Node instalado a mano en `~/.local/node-v24.x`, así que el prefijo era
esa carpeta. El CLI de Supabase estaba en `~/.local/bin` y el script del gate
(`scripts/lib/base-de-pruebas.mjs`) lo llama con `npx --no-install supabase` → la integración
cayó con `SIN_CONFIGURAR` con la base arriba. En el Mac principal funciona porque su prefijo es
`~/.local` y el bin global coincide con donde vive el CLI.

Fix: `npm config set prefix ~/.local` (va a `~/.npmrc`, lo lee cualquier shell y el servicio
del runner). Diagnóstico rápido: `npm config get prefix` en las dos máquinas.
