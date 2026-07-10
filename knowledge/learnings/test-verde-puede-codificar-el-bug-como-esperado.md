---
title: un test en verde puede estar codificando el bug como comportamiento esperado
date: 2026-07-11
source: claude-code-session
tags: [tdd, testing, auditoria]
---
Al corregir un bug confirmado por auditoría, varios tests fallaron — no por regresión, sino porque el test original hacía `expect()` sobre el valor BUGGY (p. ej. "c13 se acota a c12" o "DOS registros por %" cuando la norma exige uno). Gate 100% verde no prueba que el comportamiento sea correcto si el propio test fue escrito copiando el output del código, no derivado de la norma/spec independientemente.

**Cómo lo detecté**: recomputación ciega (un agente que calcula a mano desde la norma, sin leer el calculador) contra el output real — cualquier discrepancia es candidata a bug, incluso con tests en verde.

**Al arreglar**: no solo cambiar el código — releer CADA test que fallé para confirmar que codificaba el bug (no una regresión real) antes de reescribir su expectativa. Mismo criterio para fixtures usados en varios tests: si cambias una escena, verifica todos sus consumidores antes de aceptar el nuevo output como "correcto".
