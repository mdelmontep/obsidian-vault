---
title: aseverar un orden de inserción que la consulta no define, y los dos arreglos que no valen
date: 2026-08-17
updated: 2026-08-17
source: claude-code-session
tags: [postgres, testing, flakiness, sql]
---

Un test que lee N filas con `ORDER BY created_at` y compara una **lista** asevera un orden que la
consulta no define en cuanto dos valores empaten: lo decide el plan y el orden físico. Sale verde casi
siempre → se lee como flake del entorno.

⚠️ **Corregido el 17-ago (noche) al implementarlo: la versión anterior de esta nota era FALSA en dos
puntos, y los dos cambian el arreglo.**

- ❌ *«las N filas comparten `created_at` por ir en la misma transacción»*. **Medido: NO.** Si cada
  write entra por su propio request son N transacciones y N instantes — `899371 · 910624 · 918829 ·
  927039`, separados 8-11 ms. El empate **no es sistemático: es una carrera** que se gana casi
  siempre, y por eso el rojo parece ambiental. «Un audit por write en la misma tx» significa que cada
  write va con SU audit, no que los N compartan una.
- ❌ *«fix: `ORDER BY created_at, id`»*. **No vale si el `id` es `gen_random_uuid()`**: da un orden
  definido pero **arbitrario**, no la secuencia de inserción. Sin columna de secuencia el orden de
  inserción **no es reconstruible por consulta**, y meter un `BIGSERIAL` en una tabla de auditoría es
  una decisión de esquema que un test no toma solo.

✅ **Lo que sí vale**: separar las dos propiedades que la lista mezclaba. **QUÉ** hay → ordenar por una
columna sin repetidos. **EN QUÉ ORDEN** → comparar los timestamps **por valor** y no por posición, con
`<=` y no `<`. Así no se pierde la propiedad que se temía perder al comparar conjuntos.

🔬 **El contrafáctico se FABRICA**: esperar a que la carrera se pierda es una lotería (el caso pasa
igual con el defecto puesto). Insertar N filas con el mismo instante y en orden físico invertido hace
las dos aserciones distinguibles. Hermano: [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]].
