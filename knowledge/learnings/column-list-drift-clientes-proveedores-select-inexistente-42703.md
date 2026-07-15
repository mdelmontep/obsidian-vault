---
title: lista de columnas hardcodeada con una columna que la tabla no tiene → 42703 y helper que traga el error degrada a comportamiento silencioso
date: 2026-07-15
source: claude-code-session
tags: [supabase, postgrest, facturaia, holded, parse-dont-validate]
---
Dos tablas casi-gemelas (`clientes`/`proveedores`) NO tienen las mismas columnas:
`clientes` tiene `updated_at` y `telefono_e164`; `proveedores` ninguna. Reusar
una constante de columnas de una en la otra (`PROVEEDOR_COLS` copiada de
`CLIENTE_COLS`) → PostgREST **42703** (`column ... does not exist`) → TODA la
query falla.

El fallo silencioso lo cometió el helper: `const { data } = await …` (sin leer
`error`) devolvía `null` como si "no hubo match". El pull interpretaba "no existe
proveedor" → INSERT → choque con la unique `(org_id, lower(nif))` → error de
duplicado en cada ciclo. El síntoma (dup key) estaba a 3 saltos de la causa
(columna inexistente).

Patrón: (1) NUNCA asumir mismas columnas entre tablas parecidas — verifica
`information_schema.columns` al copiar un select. (2) Un helper de query que
ignora `error` convierte un fallo duro en comportamiento erróneo silencioso →
lee `error` y haz throw. Reproducir por el MISMO cliente (supabase-js), no por
psql: psql no ve el 42703 de PostgREST. Ver [[facturaia-holded-integracion]].
