---
title: un test que recorta un bloque del hook hasta la sección siguiente se rompe al reordenar
date: 2026-09-28
source: facturaia
tags: [tests, hooks, git, rebase]
---

Un test que extrae un bloque de `.githooks/pre-push` «desde su marcador hasta el comentario de la sección siguiente» depende del ORDEN de las secciones, no del bloque. Si alguien reordena el hook (facturaia #3055 movió el candado de permisos delante del build), el recorte pasa a abarcar otras secciones, o se queda corto, sin que falle nada.

Caso: el rebase de #2838 sobre #3055 fusionó sin conflicto el test, y el CONTROL (el caso que debe dar «deja pasar») salió BLOQUEA porque el trozo recortado ya incluía otra sección.

Patrón: anclar el fin del recorte en el propio bloque (un marcador de cierre suyo), nunca en el comienzo del vecino. Y tras un rebase que toque el hook, correr esos tests y comprobar que siguen mordiendo.
