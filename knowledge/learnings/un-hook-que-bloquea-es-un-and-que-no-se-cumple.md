---
title: un hook que bloquea es un && que no se cumple, así que la limpieza no va encadenada
date: 2026-08-06
source: claude-code-session
tags: [claude-code, hooks, git, metodo]
---
Un fichero de scratch acabó commiteado en `main` **con «NO se commitea» en su primera línea**. No fue
olvido: fue encadenamiento.

    rm scratch.ts && grep -n '"evals' package.json     # el hook bloqueó el comando ENTERO

El hook (`paid-measure-guard`) matcheó `evals` con el árbol sucio — y hacía bien. Pero el `rm` era el
**primer eslabón**, así que **nunca corrió**, y un `git add -A` posterior barrió el fichero al commit.

Lo que lo hace traicionero: el bloqueo se lee como *«no hagas esto»*, no como *«tu limpieza no se ha
hecho»*. No hay señal de que quedara trabajo a medias.

**Regla: la limpieza va sola, o después.** Nunca delante de algo que un hook, un permiso o un
clasificador puedan rechazar. Y el corolario que cierra el agujero: **`git add -A` convierte cualquier
limpieza no ejecutada en un fichero en `main`** — mirar `git status` antes de commitear, no después.

Y una segunda vez el mismo día: un `cd X && rm y && ...` no es lo único; **cualquier** compuesto donde
el efecto deseado va antes del que puede fallar tiene este problema.
