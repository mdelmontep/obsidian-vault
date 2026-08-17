---
title: un registro de excepciones que no distingue caducado de vigente borra los dos
date: 2026-08-17
source: claude-code-session
tags: [gates, arnes, excepciones, metodo]
---

Los ficheros de excepciones declaradas —baselines de auditoría, trinquetes, manifiestos de capa
compartida— guardan **el porqué**, y ése es el único sitio donde vive. El comando que las acepta
suele reescribir ese campo, con buen argumento: heredar un motivo viejo dejaría una excepción de
hace tres meses leyéndose como de ayer.

El argumento vale mientras haya **una excepción por entrada**. En cuanto una entrada acumula
divergencias INDEPENDIENTES —siete sobre el mismo fichero, cada una sobre otra cosa— la séptima no
sustituye a la primera, y «el motivo viejo describe algo que ya no existe» pasa a ser falso.

Cómo se detecta que ya te ha pasado: mide la **longitud del campo commit a commit**. Debe crecer
monótonamente; el commit donde encoge es el que se llevó algo. En un caso real el registro creció
en catorce revisiones y encogió en una, y lo que sobrevivió aquel día lo salvó que la persona lo
copiara **a mano** — o sea, nada.

El arreglo no es «concatenar siempre» (eso reintroduce lo que el diseño evitaba) sino **fail-closed
con la intención declarada**: con un motivo vigente delante, el comando falla, imprime lo que se
perdería y exige `--anade` o `--reemplaza`. Sólo quien llama sabe cuál es.

Y la señal de que tienes uno: el comando **se llama `accept`**, no `replace`.
