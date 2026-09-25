---
title: reutilizar una base sembrada con un secreto aleatorio nuevo deja pantallas sin medir con «0 nuevos»
date: 2026-09-25
source: agh-iberica
tags: [testing, verificacion, falso-verde, ui, cifrado]
---
**Qué pasó (AGH #1977):** el script de verify:ui generaba una clave de cifrado aleatoria en cada corrida,
pero reutilizaba la base de UI ya sembrada con la clave de la corrida anterior. Las pantallas de
documentos cifrados fallaban con `wrong_key`, no se abrían, y el informe decía **60 cruces · 0 nuevos**
en vez de 70. Una pantalla que no se abre no produce diferencias, así que el verde estaba vacío.

**Patrón:** estado persistente + secreto efímero = el arnés mide menos, y lo dice como «sin cambios».

**Fix:**
- recrear la base en cada corrida, o fijar el secreto junto a la base que lo usó;
- antes de pegar la línea, comparar **cuánto se midió** (cruces, pantallas, tests) contra la corrida de `main`. Si baja sin que el diff quite nada, falta medición, no hay mejora.

Relacionado: [[it-each-sobre-filter-vacio-no-registra-ningun-test]] · [[agh-iberica]]
