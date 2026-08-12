---
title: variable NEXT_PUBLIC_* nueva no llega al cliente si falta el build-arg en Dockerfile/compose
date: 2026-07-16
source: claude-code-session
tags: [nextjs, docker, dokploy, env, deploy]
---

Poner una variable `NEXT_PUBLIC_*` nueva en el panel "Environment" de Dokploy (o
cualquier orquestador) y redesplegar —incluso con rebuild completo, no
cacheado— NO basta si el Dockerfile no la declara explícitamente como build-arg.
Next.js sustituye `process.env.NEXT_PUBLIC_X` en build-time (webpack/turbopack
DefinePlugin); si el Dockerfile solo pasa esa var como `environment:` en
runtime (docker-compose) pero no como `ARG X` + `ENV X=$X` en el stage que
corre `npm run build`, el valor nunca llega al bundle cliente por mucho que
redespliegues.

Síntoma: la env está bien puesta y verificada en el panel, el deploy termina
"done", pero cualquier feature que dependa de ese valor en cliente (banner de
permiso, config pública, etc.) sigue actuando como si la variable no existiera.

Fix: añadir el par `ARG NOMBRE` + `ENV NOMBRE=$NOMBRE` en el Dockerfile (stage
`builder`, ANTES de `RUN npm run build`) + `NOMBRE: ${NOMBRE}` en
`docker-compose.yml` bajo `build: args:` — mismo patrón que las vars públicas
que ya funcionan (ahí está el ejemplo a copiar, no inventar). Caso real:
`NEXT_PUBLIC_VAPID_PUBLIC_KEY` en TuFacturaIA, PR #949.

**Misma raíz, otra puerta — en LOCAL, con dos entornos (12-ago).** El destino del cliente lo fija el
`build`, no el arranque: `next start` con el entorno impecable sirve igual un bundle compilado contra
otro proyecto. Un `next build` lanzado sin las vars de staging dejó el bundle apuntando a
**producción**, y el síntoma manda a mirar donde no es: la pantalla de login contesta «Email o
contraseña incorrectos», que es literalmente cierto (ese usuario no existe en prod). Una hora. Se
comprueba el BUNDLE, no el entorno: `grep -rlo "<ref-de-prod>" .next/static | wc -l` tiene que dar 0.
Puesto como guard en `scripts/dev-staging.sh`.

Ver [[facturaia]].
