---
title: agrupación por campo de texto libre exige normalización en write path + saneo
date: 2026-06-10
source: claude-code-session
tags: [datos, normalizacion, fiscal, supabase]
---
Caso real (TuFacturaIA Modelo 349): los registros se agrupan por clave literal
`${nif_iva}|${clave}`, pero `nif_iva` era texto libre — `de 123.456.789` y
`DE123456789` partían un mismo operador en 2 registros (y rompían el umbral
50k y el hash de versión).

Fix con DOS patas obligatorias, una sola no basta:
1. **Write path**: normalizar al guardar (API clientes: uppercase + strip
   espacios/puntos/guiones) — evita datos sucios nuevos.
2. **Migración de saneo** (mig 251): `UPDATE` de los existentes con la misma
   regla — sin esto el bug persiste en datos históricos aunque el código esté bien.

Patrón general: cualquier `group-by`/`distinct`/clave compuesta sobre un campo
de texto libre necesita ambas. Relacionado: [[campo-sincronizado-entre-tablas-debe-poblarse-en-todos-los-puntos-de-escritura]].
