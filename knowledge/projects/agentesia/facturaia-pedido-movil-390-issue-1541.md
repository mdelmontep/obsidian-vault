---
title: Pedido de obra en móvil (390 px) — issue #1541 · RESUELTO
date: 2026-08-08
source: rescatado de un stash y mergeado en #1551
tags: [facturaia, obras, frontend, responsive, rescate, resuelto]
---

# Pedido de obra en móvil (390 px) — issue #1541 · RESUELTO

**Estado: en `main` desde el 8-ago-2026, commit `bc90dcd8` (PR #1551).** Esta nota
se escribió cuando el trabajo solo existía en un stash mal etiquetado, y se
corrige aquí para que no siga afirmando lo contrario.

## Lo que pasó, que es lo que merece recordarse

El trabajo vivía en un stash llamado `restos-obsoletos-rejilla-#1538-sesion-8ago`
— una etiqueta que invita a tirarlo — cuando en realidad eran 78 líneas de CSS
responsive razonado. Se rescató al verificar (`grep "max-width: 720px"`) que el
worktree `~/wt-390` estaba en `main` y **no** tenía el bloque. Copia del diff en
`facturaia-pedido-movil-390-issue-1541.patch`, junto a este archivo.

Horas después otra sesión lo mergeó por su cuenta en #1551, así que el rescate no
hizo falta. Pero la lección sí:

**`refs/stash` es por worktree, no por repositorio.** `wt-deuda` tenía su propio
stash con esta etiqueta y el repo raíz otro distinto con la MISMA, y
`git worktree remove` se lleva los refs por worktree — es decir, **borrar un
worktree puede destruir un stash** que solo vivía ahí. Se detectó porque
`git stash show --stat stash@{0}` daba 1 fichero desde `wt-deuda` y 5 ficheros
distintos desde el raíz. Corolario práctico: antes de `git worktree remove`,
`git -C <worktree> stash list`; y no fiarse de la etiqueta de un stash para
decidir si sobra — mirar el contenido.

## Qué resolvía (por si hay que volver a razonarlo)

A 390 px la fila de línea de pedido pedía 472 px (533 con la fila tocada). El
navegador móvil **no saca scroll horizontal: ensancha el layout viewport**, así
que el síntoma no es una barra sino que todo se ve más pequeño de lo debido — y
las cifras de un pedido son justo lo que no conviene leer chico.

La decisión: **los campos no se encogen.** Repartiendo las pistas `fr` a 390 px
tocaban 42 px a cantidad y 48 a precio, de los que 20 son relleno. Por debajo de
720 px la fila se parte en dos y los campos conservan sus 90 y 100 px:

```
línea 1   nombre ······································  importe
línea 2   cantidad   precio  ························  acciones
```

Detalles no obvios: la tercera pista mide `max(importe, acciones)` para que el
importe no se recorte; los rótulos se ocultan porque sin columnas alineadas
debajo no rotulan nada (ya eran `aria-hidden`); y `overflow-wrap: anywhere` en el
nombre es el seguro, porque una referencia de material larguísima empujaría las
dos primeras pistas por encima de sus 190 px.

El guard es `pedido-linea-estrecha.test.ts`, y lo que NO vigila está escrito en
`manual-admin`: no hay aritmética, porque aquí las pistas son `auto` dentro de
`grid-template-areas` y el modelo daba por buenas configuraciones que el
navegador rechazaba. Vigila lo estructural y el encaje se mide en navegador.

Relacionado: [[facturaia]]
