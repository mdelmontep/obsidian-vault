---
title: vitest sale EXIT 1 por un unhandledRejection aunque 0 tests fallen (fuga de teardown pg)
date: 2026-07-07
source: claude-code-session
tags: [vitest, testing, postgres, ci, flakiness]
---

Un run de vitest con **0 aserciones fallidas** puede salir **EXIT 1**: vitest marca el run
como fallido ante cualquier `unhandledRejection` durante la ejecución ("Vitest caught 1
unhandled error"). Una suite "verde" se ve roja y confunde el gate.

Caso real (agh-iberica): un test de BD efímera dropea su base (`DROP DATABASE agh_migrator_test`)
con una conexión `pg` aún abierta → el server la termina → `57P01 terminating connection due to
administrator command` como rejection sin handler. Intermitente: dependía del paralelismo
(`--maxWorkers=3` lo disparaba, `--maxWorkers=2` daba EXIT 0 limpio).

- Diagnóstico: buscar "Unhandled Errors"/"originated in <fichero>" en el output, NO el resumen
  de tests (que dice 0 fail).
- Mitigación inmediata: bajar workers (`--maxWorkers=2`) reduce la carrera.
- Fix de raíz: cerrar TODO pool/conexión (`await pool.end()`) antes del `DROP DATABASE`, o
  `pg_terminate_backend` sobre la datname. Distinto de [[vitest-fileparallelism-false-tests-integracion-bd-compartida]]
  (colisión entre ficheros que comparten BD) — aquí es fuga de teardown de una BD efímera.
