---
title: pgTAP tests para triggers SQL del subsistema Conciliación
date: 2026-05-21
tags: [inbox, facturaia, tests, postgres]
---

Gap estructural detectado tras self-review PR #73: hay ~16 migraciones
encadenadas en Conciliación (061, 101, 103, 106, 109, 111, 112-117, 128,
131-141) y ningún test SQL automatizado pre-deploy. Toda validación
hasta hoy = smokes ad-hoc via DO blocks contra sandbox.

Bugs encontrados que un test pgTAP habría capturado pre-deploy:
- mig 137: BEFORE INSERT + ON CONFLICT cuenta fila fantasma.
- mig 138→139: vector evasión via UPDATE metodo='automatico'.
- mig 140→141: cascade guard incompleto (2 de 4 triggers).
- mig 141: cron top-N+filter-JS nunca procesa antiguos.

Stack candidato:
- `pgtap` extension via Supabase (test framework SQL nativo).
- CI job que aplica migs en BD efímera + corre `pg_prove`.
- Fixtures reusables: org sandbox + factura + mov por escenario.

ROI: tras 18 smokes ad-hoc hoy + 4 hotfixes encontrados pos-merge, vale.
