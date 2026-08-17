---
title: docker compose deriva el proyecto del directorio, y en un repo con worktrees eso levanta un clúster vacío
date: 2026-08-17
source: claude-code-session
tags: [docker, compose, worktree, postgres, volumenes]
---

Sin `name:` de nivel superior, Compose deriva el **nombre de proyecto** del **nombre del directorio**,
y los volúmenes se resuelven como `<proyecto>_<volumen>`. En un repo que se trabaja con **un worktree
por issue**, eso significa un volumen distinto por worktree:

```
raíz del repo   -> agh-iberica_pgdata   (no existe)
~/wt-1064       -> wt-1064_pgdata       (no existe)
con  name: agh  -> agh_pgdata           <- el que tiene los datos
```

**El daño no es «no arranca»: es que arranca.** `docker compose up -d` crea el volumen que falta,
hace `initdb` y sirve un Postgres **vacío** en el mismo puerto, dejando el bueno huérfano. El síntoma
—bases que no existen, tests de integración en rojo— **es idéntico al de una regresión del propio
diff**, así que se depura el código durante un rato. En agh-iberica la doc del repo llegó a
**recomendar por escrito** la receta que lo provocaba (`compose down` allí, `up -d` aquí).

**Fix**: `name: <proyecto>` en el `docker-compose.yml`, no `COMPOSE_PROJECT_NAME` en el entorno —
el env se olvida y el fichero viaja con el repo. Y si el contenedor vivo se creó a mano con
`docker run -v <vol>:...`, **elige el `name:` que reproduzca ese nombre** y compose lo adopta:
avisa `volume already exists but was not created by Docker Compose` y **continúa** (es un warning;
comprobado con `--dry-run`).

**Dos trampas al adoptar un contenedor creado a mano:** el `restart:` (compose por defecto es `no`,
así que si el original tenía `unless-stopped` lo pierdes en silencio) y `up -d` **sin nombrar
servicios**, que construye todo lo demás que declare el fichero.

Candado barato: un test que asevere la **relación** —`name` + volumen == el volumen real—, no la
presencia de un `name:` cualquiera.

Misma raíz que [[hook-en-worktree-efimero-no-debe-derivar-nombre-de-basename-cwd]]: derivar identidad
del path es frágil en cuanto hay worktrees.
