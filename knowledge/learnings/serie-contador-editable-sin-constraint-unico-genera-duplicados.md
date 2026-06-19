---
title: contador editable de numeración sin constraint único genera duplicados
date: 2026-06-19
source: claude-code-session
tags: [facturaia, supabase, fiscal, data-integrity]
---

Un campo UI que fija un **contador monótono** de numeración documental (lo
incrementa un RPC al emitir), sin constraint único en BD sobre
`(org_id, serie, num)`, permite **bajar** el contador → el siguiente documento
reusa un número ya emitido = **duplicado** (ilegal, correlatividad RD 1619/2012).

Síntoma reportado por usuario: "pongo numeración 10, vuelvo a 9, ¿genera otra 10?"
→ sí, y nada en BD lo impide.

- **Fix mínimo (app)**: guard en el `PATCH` — rechazar `contador < actual` si
  la serie ya se usó (`actual > 0`); subir (migración) se permite. Espejo en el
  form (input `min`, aviso, save bloqueado). Mismo criterio "usada" que el DELETE.
- **Fix duro (aplicado)**: índice único **parcial** sobre `(org_id, serie, num)`
  excluyendo borradores/no-emitidos (facturas además `tipo='emitida'` para no atrapar
  recibidas). #420 / mig `343`, aplicado a prod 2026-06-19 (0 duplicados previos verificados).

Caso: modal *Editar serie*, TuFacturaIA #414 (guard app) + #420 (índice BD). Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] (cómo se entregó vía worktree con la paralela activa; el `db push` exigió `migration repair` de 5 orphans timestamp de la paralela).
