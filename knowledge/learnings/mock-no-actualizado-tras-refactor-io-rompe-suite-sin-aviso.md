---
title: correr el test file solo antes de extenderlo — puede estar ya roto en main
date: 2026-06-30
source: claude-code-session
tags: [testing, vitest, refactor]
---

Un refactor que cambia la forma de hacer I/O (ej. pasar de recibir el media en el body a
descargarlo de Storage) puede dejar el mock de un test desincronizado sin que nadie lo note:
el test sigue "verde" en CI si nadie vuelve a tocar ese archivo, pero en realidad está 100%
roto (falla por una excepción no relacionada con lo que el test pretende verificar).

Caso real: refactor de `ocr-process` para descargar el documento de Storage en vez de recibirlo
en el body dejó 34/34 tests fallando con 422 ("documento_url no encontrado") — el mock de
`createAdminClient` nunca simulaba `documento_url` ni `.storage.from().download()`.

**Fix/patrón**: antes de añadir tests nuevos a un archivo (TDD u otro), correrlo solo primero
(`vitest run <archivo>`). Si ya está roto, arreglar el mock es un prerequisito, no scope creep —
sin eso, un test nuevo en rojo no distingue "falta implementar" de "harness roto".
