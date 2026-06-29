---
title: postgrest columna inexistente en select retorna 400 data=null sin error descriptivo
date: 2026-06-29
source: claude-code-session
tags: [supabase, postgrest, debugging, schema]
---

## Qué pasa

PostgREST devuelve HTTP 400 y el cliente JS de Supabase recibe `data = null`, `error = null`
(o un error genérico sin indicar qué columna falla) cuando el SELECT incluye una columna
que no existe en esa tabla concreta.

## Por qué es peligroso

El código comprueba `if (!data) throw new Error('No encontrado')` → el error llega
al usuario como "no encontrado" en vez de "schema incorrecto". Silencioso y confuso.

## Caso real

`duplicarPresupuesto` seleccionaba `forma_pago` de la tabla `presupuestos`.
Esa columna solo existe en `facturas`. Preview no fallaba (no hacía ese SELECT);
execute sí. Síntoma: preview OK, confirm → "No he encontrado ese presupuesto".

## Fix / patrón

- Cruzar columnas del SELECT con las migraciones de la tabla específica, no la "hermana".
- En arquitecturas two-table (`facturas` / `presupuestos` como subset), los campos
  exclusivos de la tabla mayor nunca deben aparecer en el SELECT de la menor.
- Si necesitas forma_pago en presupuestos legacy: comprueba antes de asumir.
