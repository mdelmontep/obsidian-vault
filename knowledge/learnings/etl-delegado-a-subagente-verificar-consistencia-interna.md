---
title: etl delegado a subagente — verificar consistencia interna, no solo conteos
date: 2026-07-21
source: claude-code-session
tags: [subagentes, etl, migracion]
---
Delegué la extracción de 130k partidas a un subagente; los conteos y los totales por
`presupuesto_id` cuadraban, PERO el `nodo_key` de cada fila era inconsistente con su
`presupuesto_id` (extraídos por joins distintos). Al cargar enlazando por `nodo_key`, las
partidas colgaron de presupuestos equivocados → totales mal, y costó mucho aislarlo porque
la validación "por etiqueta" pasaba.

Regla: al usar output de un subagente para ETL, verifica la **consistencia CRUZADA entre campos
de la misma fila** (aquí: que la clave de enlace y la de agrupación salgan del MISMO join), no
solo conteos y sumas agregadas. Y para datos críticos de paridad, re-extrae tú la pieza clave
en vez de fiarte del agente. Ver [[migrar-precios-erp-congelar-neto-con-aritmetica-del-origen]].
