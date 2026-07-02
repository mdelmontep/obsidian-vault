---
title: integrar con una interfaz de otra PR no mergeada por tipado estructural
date: 2026-07-02
source: claude-code-session
tags: [typescript, monorepo, parallel-work]
---

Varias PRs en paralelo sin mergear (AGH: #8, #11, #14). Cuando tu PR necesita "servir" una interfaz definida en otra que aún NO está en `main` (p.ej. `FunnelConfig` de #8), **no la importes** — `import type` de un fichero ausente rompe `tsc --noEmit` (el gate) y bloquea tu PR.

Fix: implementa una clase con **la misma firma de métodos** y documéntalo. TS es estructural → satisface la interfaz sin `implements` ni import cuando la otra PR mergee; el cableado real (`implements` + registrar) queda como 1 línea diferida con nota.

Ojo **sync vs async**: si la interfaz es síncrona (`stages(t): string[]`) pero el dato vive en Postgres, hidrata una vez en factory `load()` y sirve síncrono desde un Map. Para tablas de otras PRs en un reset: `to_regclass` skip-missing → forward-compatible. Ver [[audits-cross-pr-vs-per-pr]].
