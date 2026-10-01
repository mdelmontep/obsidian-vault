---
title: el loadavg de macos cuenta los hilos de los propios jobs, y un semáforo que lo usa se autobloquea
date: 2026-10-01
source: harness ~/.claude (fia-gate, commit e5cee86)
tags: [fia-gate, macos, rendimiento, gates]
---
- `vm.loadavg` en macOS cuenta hilos ejecutables, incluidos los de los jobs que el semáforo YA admitió (vitest, tsc, next build abren muchos).
- Con `carga < cores*0,85` como condición para abrir la plaza extra, la abrían los propios jobs al cerrarse: abierta 0,4 h en cuatro días.
- Fix: la plaza por encima del suelo la decide la memoria (sin un job `mem` corriendo y sin presión: `kern.memorystatus_level`, `vm_pressure_level`), que sí mide lo que satura.
- Dejar la carga como dato informativo en el panel, nunca como puerta.
- Relacionado: [[el-suelo-de-un-semaforo-explica-quien-entra-no-cuanto-tarda]].
