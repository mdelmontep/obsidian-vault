---
title: dos catálogos exportados del mismo SaaS pueden contradecirse
date: 2026-08-30
source: agh-iberica
tags: [migracion, importador, datos, yooz]
---
Yooz exporta el plan contable y el maestro de proveedores como dos tablas independientes.
En AGH (235 cuentas, 40 proveedores) no cuadran entre sí:
- `IBEBUXS02` e `IBEOVH999` tienen **nombre distinto en cada fichero**.
- Tres códigos de proveedor del plan (`1`, `2`, `3`) no existen en el maestro.
- BLUUMI (`41000000562`) está en el maestro y **no** en el plan.
- Hay una cuenta `GASTO (test)` y cinco localizadores de Iberia usados como código de cuenta.

Un importador que fusione en silencio hereda la basura y la vuelve verdad en el sistema
nuevo. El patrón que funciona son **dos fases sobre el mismo endpoint**: `?fase=analizar`
no escribe y devuelve las incidencias clasificadas; `?fase=aplicar` recibe las exclusiones
confirmadas y escribe en transacción. La clasificación por defecto excluye, nunca inventa.

La migración es el único momento en que alguien mira esos datos. → [[facturaia-yooz-agh-migracion]]
