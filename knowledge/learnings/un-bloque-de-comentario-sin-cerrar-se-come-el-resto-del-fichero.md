---
title: un quitacomentarios casero toma un /* sin cerrar por comentario y se come el fichero
date: 2026-09-13
source: facturaia
tags: [parsers, trinquetes, metricas]
---
Los contadores que miden código (líneas, variables de entorno, antipatrones) quitan primero
los comentarios. Si el tokenizer trata `/*` como apertura sin comprobar que existe `*/`
detrás, un texto normal lo dispara: `` `muévela fuera de /api/admin/*.` `` dentro de un
template, o una regex. A partir de ahí se come **todo el resto del fichero**: un fichero de
80 líneas medía 43, y el trinquete llevaba meses contando de menos sin fallar nunca.

- Fix: `const fin = src.indexOf('*/', k + 2); if (fin < 0) trátalo como texto` — un `/*` sin
  cierre no puede ser un comentario, porque el fichero no compilaría.
- Límite que queda: un `/*` dentro de comillas invertidas CON un `*/` más abajo sigue
  colándose; el tokenizer tendría que seguir los backticks.
- Señal: un contador que da un número redondo o sospechosamente bajo y nunca sube.
  Contrástalo con una medida de otra naturaleza antes de publicarlo.
