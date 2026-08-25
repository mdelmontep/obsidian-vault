---
title: un check que muere en segundos sin ejecutar pasos es la plataforma, no tu código
date: 2026-08-25
source: agency-portal
tags: [github-actions, ci, diagnostico]
---
`gh pr checks` daba `verify fail` en agency-portal y la lectura inmediata fue
«algo del PR». No: el CI del repo lleva roto desde el **17-ago** y nadie lo vio
porque los PRs se mergean igual.

Los tres datos que lo cierran en 30 s, todos con `gh`:
- `gh run list --limit 60 --json conclusion` → **56 fallos / 4 éxitos**, el
  último verde el 17-ago.
- Duración: `createdAt` → `updatedAt` de **3 segundos**, y `.jobs[].steps` vacío.
  Un job que falla sin ejecutar un solo paso no ha llegado a tu código.
- Falla también en **`main`**, en pushes que no son de nadie en concreto.

Eso es cuota de Actions o límite de gasto de la organización (confirmarlo pide
scope `admin:org`, que un PAT normal no trae). Mientras dure, **los gates solo
valen corridos en local** y hay que decirlo al pedir un merge: si no, el
reviewer lee el check rojo como «el código está mal» y se bloquea la cadena.

Corolario: antes de depurar un check en rojo, mira si `main` lo tiene rojo
también. Un fallo que no discrimina entre ramas no es de la rama.
