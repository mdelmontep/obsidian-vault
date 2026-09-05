---
title: un plan que nadie cita no existe, y puede contradecir al que sí se lee
date: 2026-09-05
source: facturaia
tags: [documentacion, metodo, prompts]
---
Escribí un prompt de continuación de 700 líneas, lo revisé con un subagente y lo di por
entregado. Antes de commitear medí quién lo citaba: **cero**. La tabla de rutas del
`CLAUDE.md` mandaba a otro fichero para esa misma área.

Lo grave no era el huerfanato, era que **los dos decían cosas opuestas**: el enrutado
decía «sin recuento no se toca nada» y el mío era un plan para reparar ya. Una sesión
fresca abre el enrutado y no llega a ver el otro nunca.

- **Antes de dar por entregado un documento**: `grep -rl "<nombre-del-fichero>"` por el
  árbol. Si sale 0, o lo enrutas o no existe.
- **Y comprueba qué dice el que YA está enrutado sobre lo mismo.** Dos documentos vivos
  sobre un área no se suman: el que gana es el que abre la tabla de rutas.
- El arreglo no fue borrar uno, fue **partir la afirmación**: qué parte del trabajo no
  necesita el dato que falta y qué parte sí.

Ver [[auditar-una-doc-por-identificador-no-por-seccion]] · [[una-lista-de-hallazgos-caduca]]
