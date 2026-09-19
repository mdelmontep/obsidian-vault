---
title: un desempate de order by necesita un fixture que decida por cada cláusula
date: 2026-09-19
source: agh-iberica
tags: [testing, sql, mutacion]
---
Un test de «el vigente es el más reciente» con `ORDER BY fecha DESC, created_at DESC, id DESC` puede salir verde con una cláusula que no hace nada: si el más reciente por `created_at` también tiene el id mayor, quitar `created_at` elige al mismo ganador.

- Patrón: por cada cláusula del desempate, el fixture debe hacer que quitarla o invertirla cambie el resultado. Por ejemplo, dar el id MAYOR al evento que debe PERDER por `created_at`.
- Medirlo, no suponerlo: los mismos datos contra la consulta original y contra una mutante por cláusula, en psql dentro de `BEGIN … ROLLBACK`.
- Si la consulta vive en una migración ya registrada, el arnés de mutación no sirve: cambiar el fichero cambia su checksum, la precarga de la suite aborta y sale «ARNÉS ROTO», que no dice nada del test.

Caso: agh-iberica #1875, vista `consultant_current_salary`. Sin `created_at`, la mutante daba 42000 igual que la original; con el fixture corregido da 40000.
Ver [[un-test-de-una-barrera-que-otra-barrera-tambien-para-no-la-discrimina]].
