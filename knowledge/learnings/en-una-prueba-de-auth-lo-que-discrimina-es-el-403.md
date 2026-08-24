---
title: en una prueba de auth lo que discrimina es el 403, no el 200
date: 2026-08-24
source: panel-tecnocloud
tags: [n8n, webhooks, seguridad, smoke-tests]
---

Al cerrar un webhook de n8n con `headerAuth`, el script comprobaba «sin cabecera → 403» y
«con cabecera → **200**». La segunda dio **400** y el script cantó fallo y pidió revertir un
despliegue que estaba bien: el 400 lo devolvía el propio workflow («tool no reconocida»), o sea
que la petición **había atravesado la auth**.

- El caso de prueba se eligió a propósito sin efectos (una tool inexistente), y justo por eso no
  puede devolver 200. La prueba pedía lo que su propio diseño impedía.
- Lo que discrimina la auth es **el 403**: sin cabecera tiene que salir, con cabecera no. Cualquier
  otro código ya es la app hablando.
- Después, una prueba con una tool **real y sin efectos** (una consulta de solo lectura) para ver
  el 200 de verdad. Las dos pruebas miden cosas distintas; no las mezcles en un aserto.
- Un smoke test que falla en verde cuesta un rollback innecesario; el mío pedía restaurar el
  backup del workflow.
