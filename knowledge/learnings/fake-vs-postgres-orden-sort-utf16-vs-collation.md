---
title: fake in-memory vs Postgres divergen en orden — .sort() UTF-16 ≠ collation
date: 2026-07-02
source: claude-code-session
tags: [testing, postgres, fakes]
---

Store con doble impl (fake in-memory + Postgres real). El fake ordenaba con `.sort()` crudo de JS (por code-unit UTF-16: mayúsculas antes que minúsculas) y Postgres con `ORDER BY` (collation de la BD, case-insensitive-ish).

`["Zebra","apple","Banana"]` → PG: `apple, Banana, Zebra` · JS `.sort()`: `Banana, Zebra, apple`. Divergencia real → un test que asserta orden pasa contra un store y rompe contra el otro (el bug de "dos fakes divergentes" que el patrón fake+real existe para evitar).

Fix: usar `.sort((a,b)=>a.localeCompare(b))` en el fake para casar la collation. No lo cazan los tests si solo usas valores lowercase de un elemento — muerde con mixed-case. Test de paridad con datos mixed-case como candado.

**La regla general (3 casos en una semana en AGH, 30-jul): si la propiedad depende de que el dato CRUCE la BD, el test es `.pg` o no prueba nada.** El fake guarda el objeto tal cual; el store real serializa, parsea y valida, y ahí vive el bug. Casos: un puntero JSONB que se escribía bien y se leía `undefined` porque la whitelist de runtime listaba 5 de 6 variantes del tipo (#674, con el e2e in-memory en verde) · el `23503` que solo dispara una FK, inexistente en memoria (#643) · un fake que emitía un formato de fecha que el cliente real nunca produce (#585). Olor a buscar: un test que afirme **durabilidad, unicidad, atomicidad o parseo** sin `.pg` en el nombre.

Relacionado: [[whitelist-runtime-que-espeja-una-union-derivala-de-un-record]] · [[tests-pg-self-skip-levantar-pgvector-local]].
