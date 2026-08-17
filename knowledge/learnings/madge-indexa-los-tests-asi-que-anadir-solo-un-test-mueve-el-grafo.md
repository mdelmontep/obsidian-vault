---
title: madge indexa los tests, así que añadir SOLO un test mueve el grafo de dependencias
date: 2026-08-17
source: claude-code-session
tags: [madge, gates, facturaia, gotcha]
---

En FacturaIA el `pre-push` aborta si `docs/architecture/graphs/dependencies.json` ya no describe el
código. `madge` escanea `src` entero, **incluidos `__tests__/` y `__integration__/`**, así que un PR
cuyo diff es «solo un test» **también** mueve el grafo y te para el push.

Es contraintuitivo por dónde te pilla: el razonamiento «no he tocado código de producción, esto no
puede cambiar el grafo» suena a sentido común, y lo pagas con el diff cerrado y la cabeza en otra
cosa. Verificado dos veces el 17-ago, en dos sesiones paralelas y con PRs distintos.

Fix: `npm run deps:json && npm run deps:image` y commitear el resultado, aunque el cambio sea un
único fichero de test. El nodo entra con `[]` si el test solo importa `vitest` y librerías externas.

Al rebasar sobre una rama que también regeneró el grafo, el conflicto sale en el **SVG** (el `.json`
suele mezclar solo). Resuélvelo con la versión de la otra rama y **regenera después de rebasar**, no
antes: resolver un XML generado a mano no tiene ningún sentido.

El hook pide además **mirar** lo que revela, no solo regenerarlo. Para eso, `deps:circular` a solas no
sirve: sale con ciclos y no sabes si son tuyos. Córrelo también en `main` y compara el recuento — 15 y
15 convierte «hay ciclos» en «no he añadido ninguno», que es la afirmación que querías.

Ver [[madge-ciclo-import-dinamico-no-rompe-arista]] · [[un-agente-muerto-puede-dejar-un-motor-desacoplado-vivo]].
