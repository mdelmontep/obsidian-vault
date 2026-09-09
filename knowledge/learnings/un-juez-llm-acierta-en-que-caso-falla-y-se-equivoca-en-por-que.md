---
title: un juez LLM acierta en QUÉ caso falla y se equivoca en POR QUÉ
date: 2026-09-09
source: centro-elphis
tags: [evals, llm, testing, retell]
---
El juez de la suite marcó bien el caso 06 como fallo, y explicó mal la causa: «el agente
prioriza pedir el nombre sobre responder». En el transcript el nombre estaba impecable —lo
pedía dos veces, dentro del límite, y siempre *después* de responder—. Lo que fallaba era
otra cosa: ignoraba una pregunta directa para lanzar su pregunta de guion.

**El veredicto es una señal fiable de dónde mirar y una hipótesis no fiable de qué arreglar.**
Haberle hecho caso habría llevado a tocar la parte del prompt que funcionaba, dejando el
defecto intacto y probablemente rompiendo lo que sí estaba bien.

La pista de que el juez patina: contradice al transcript en un detalle **contable** (cuántas
veces pidió el nombre, si respondió o no). Eso se verifica leyendo, sin criterio. Cuando el
mismo caso se corre dos veces, comparar las dos explicaciones también delata — aquí la segunda
describía la causa correcta y la primera no.

Ver [[la-transcripcion-de-un-test-que-pasa-es-donde-esta-el-defecto-que-nadie-mide]]
