---
title: cap (.limit) en un id-set que alimenta una agregación infra-reporta en silencio
date: 2026-07-19
source: claude-code-session
tags: [supabase, postgrest, rendimiento, correctitud]
---
Poner `.limit(N)` a una query cuyo resultado es una LISTA visible (o un mapa
id→nombre) es defensa razonable: como mucho degrada cosmético (filas de más no
se ven). Pero el MISMO cap sobre un id-set que luego alimenta una AGREGACIÓN
(`IN(ids)` → SUM/COUNT aguas abajo) corrompe el número: el total sale
infra-reportado y NADIE se entera (no hay error, solo una cifra más baja).

Regla: antes de capear un `select('id')`, pregunta para qué se usa el set.
- Listado / mapa id→nombre → cap OK (o mejor, paginar).
- Fuente de una agregación → NO capear; si escala mal, agrega en la BD por
  `org_id` en vez de traer ids y hacer `IN()`.
Caso real FacturaIA (obras/informes/resumen): copié el `LIST_HARD_CAP=2000` de
`materiales` a la query que alimentaba `resumenObras(ids)` → totales de informe
truncados. Lo cazó `/fia-cierre`. Fix: quitar el cap solo en la agregación.
Si un cap es inevitable, emite una señal (`truncated: true`), nunca silencioso.
