---
title: en plpgsql, `array || 'literal'` se resuelve como array||array y revienta
date: 2026-07-28
source: claude-code-session
tags: [postgres, plpgsql, migraciones, gotcha]
---

Concatenar un literal a un `text[]` sin cast falla en ejecución con
`malformed array literal: "extensions"` (SQLSTATE 22P02). El literal es de tipo
`unknown` y Postgres prefiere el operador `anyarray || anyarray` sobre
`anyarray || anyelement`, así que intenta parsear la cadena como un array.

```sql
v_new := v_new || 'extensions';        -- 22P02
v_new := v_new || 'extensions'::TEXT;  -- correcto
```

No se ve leyendo el SQL: la migración parece impecable y revienta al aplicarla.
Caso real: la mig 581 de TuFacturaIA, cazada solo porque se probó contra un
`db reset` completo antes de tocar producción.

**Regla**: toda migración con un bloque `DO` se ejecuta al menos una vez contra
una base real antes de mergear. Revisarla a ojo no basta.
