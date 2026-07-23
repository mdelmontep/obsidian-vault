---
title: dos funciones que matchean el mismo texto contra los mismos alias deben normalizar igual
date: 2026-07-23
source: claude-code-session
tags: [parsing, bugs, facturaia]
---

Un parser de extractos bancarios (TuFacturaIA) tenía dos funciones distintas comparando cabeceras CSV contra la misma lista de alias (`fecha`, `f.valor`, `f.operacion`...): una (`findCol`, matching por columna) normalizaba con una función `squashHeader` (quita acentos/puntuación/espacios); la otra (`hasDateLikeHeader`, decide QUÉ FILA es la cabecera) comparaba texto crudo en minúsculas con `.includes()`.

Una cabecera real ("F. Valor", con espacio tras el punto) no matcheaba el alias `f.valor` (sin espacio) en la función sin normalizar → la fila de cabecera real nunca se detectaba, y el parser caía a un fallback erróneo (primera fila con separadores = metadatos del banco). Bug real en prod, no cazado hasta que un cliente subió un extracto con esa cabecera exacta.

**Patrón general**: si dos funciones matchean el mismo dato contra el mismo vocabulario de alias, deben usar EXACTAMENTE la misma normalización — no basta con que una de las dos esté bien. Al añadir un segundo punto de matching sobre alias ya existentes, reusar la función de normalización, no reimplementar `.includes()` a mano.
