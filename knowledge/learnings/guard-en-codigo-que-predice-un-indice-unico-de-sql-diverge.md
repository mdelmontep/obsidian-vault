---
title: un guard en código que predice un índice único de sql acaba mirando otro universo
date: 2026-07-29
source: claude-code-session
tags: [postgres, indices, dedup, multi-tenant, type-safety]
---
Cuando la unicidad la impone un **índice de Postgres** y el guard que la anticipa vive en **TypeScript**, la normalización está escrita **dos veces, en dos lenguajes** — y eso ES el bug, no un detalle de estilo. El guard no es la regla: es una *predicción* de la regla, y toda predicción diverge.

Caso real (agh-iberica #640, fallo en prod): índice `(tenant_id, lower(immutable_unaccent(trim(name))))` pero el dedup consultaba `list(tenantId, ownerUserId)` con un `normalize()` propio. Dos desalineaciones a la vez — **alcance** (tenant vs owner) y **normalización** — así que con la cuenta ya dada de alta por otro usuario el guard decía «no hay duplicado» y el `INSERT` moría con un `23505` crudo que reventaba el turno entero.

Reglas:
- La consulta del guard debe usar **literalmente la expresión del índice** (`WHERE lower(immutable_unaccent(trim(name))) = lower(immutable_unaccent(trim($2)))`), sin el `WHERE` extra que el índice no tenga. Así no pueden discrepar por construcción, y el planner resuelve con ese mismo índice.
- Devolver lo **mínimo** (`boolean`, no la fila): si el guard cruza un límite de privacidad — aquí, cartera de otro comercial — el tipo es la primera defensa; lo que no viaja no se filtra.
- Fijarlo con un test contra el **índice real** (`*.pg.test.ts`). Los tests con listas construidas a mano hornean justo la premisa falsa → [[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]].
- Detección proactiva: listar índices únicos y comparar su expresión **y su tupla de columnas** contra el `WHERE` del código que intenta evitarlos.
