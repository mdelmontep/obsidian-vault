---
title: Smoke fixtures van al repo (docs/runbooks/smokes/), no a ~/Desktop
date: 2026-05-20
source: facturaia smokes conciliacion 115/116/117
tags: [smoke, fixtures, ops, claude-code]
---

# Patrón

CSVs/SQL de smoke test guardados en `~/Desktop` se evaporan entre sesiones de Claude (instancias distintas, máquinas distintas, `/tmp` purgado). Recrear los inputs cada vez es ruido + riesgo de divergencia.

# Convención

`docs/runbooks/smokes/<área>/`:
- Fixtures input (CSV, JSON).
- `postcheck.sql` con placeholders `:org_id`.
- `README.md` con steps + esperado por smoke.

Commit con la PR del feature. Referenciar desde hub. PII real NO entra — generar sintéticos.

# Excepción

Outputs efímeros (snapshots de un run concreto) sí pueden vivir en `~/Desktop` o `/tmp`. Solo el **input reproducible** va al repo.
