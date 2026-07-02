---
title: fake in-memory vs Postgres divergen en orden — .sort() UTF-16 ≠ collation
date: 2026-07-02
source: claude-code-session
tags: [testing, postgres, fakes]
---

Store con doble impl (fake in-memory + Postgres real). El fake ordenaba con `.sort()` crudo de JS (por code-unit UTF-16: mayúsculas antes que minúsculas) y Postgres con `ORDER BY` (collation de la BD, case-insensitive-ish).

`["Zebra","apple","Banana"]` → PG: `apple, Banana, Zebra` · JS `.sort()`: `Banana, Zebra, apple`. Divergencia real → un test que asserta orden pasa contra un store y rompe contra el otro (el bug de "dos fakes divergentes" que el patrón fake+real existe para evitar).

Fix: usar `.sort((a,b)=>a.localeCompare(b))` en el fake para casar la collation. No lo cazan los tests si solo usas valores lowercase de un elemento — muerde con mixed-case. Test de paridad con datos mixed-case como candado.
