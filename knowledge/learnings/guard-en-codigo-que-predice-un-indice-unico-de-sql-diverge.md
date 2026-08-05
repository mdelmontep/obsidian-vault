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

**Y aunque el guard sea correcto, no sirve si hay hueco temporal entre consultarlo y escribir.** En un
flujo propose→confirm (agh #875) pasan **turnos enteros** entre los dos, así que el nombre puede
entrar por otra vía en medio. Repetir la consulta antes del `INSERT` **estrecha la ventana pero no la
cierra** (sigue siendo read-then-write) y duplica otra vez la normalización. El índice es el **único
árbitro sin carrera**: dejarlo hablar y **traducir su `23505` a un error tipado de dominio** en la capa
que conoce el driver, con la misma copia honesta que ya da el camino de propose. Comprobar el
`constraint`, no solo el código: mapear cualquier `23505` de la tabla a «ese nombre ya existe» dice una
**mentira concreta**, que es peor que un genérico. Y ojo a la taxonomía de errores: la clase nueva no
puede caer en el cajón de otra causa (allí, todo `UserFacingError` se contaba como `auth_expired`, así
que los duplicados se habrían contado como fallos de autenticación).
