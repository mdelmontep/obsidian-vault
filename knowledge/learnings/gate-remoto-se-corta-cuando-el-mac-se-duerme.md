---
title: gate-remoto se corta cuando el mac se duerme, no por la vm
date: 2026-10-16
source: facturaia (auditoría, trenes 2-3)
tags: [gate, vm, macos, harness]
---
- Síntoma: «✘ gate-remoto: se cortó la conexión con gates a mitad del gate» (código 3); el pre-push lo reporta como «errores de TypeScript». La VM termina en verde por su lado, pero el verde no se importa.
- Causa: el Mac va con batería y entra en sueño (`pmset -g log`: Sleep 20:51→21:18…). Cae el ssh. No es carga: la VM tenía 38 GB libres y respondía.
- Fix: `caffeinate -is <gate-remoto|git push>`. Con la tapa cerrada no basta: enchufar o tapa abierta.
- Tell: dos sesiones cortadas a la vez a la misma hora.
- Relacionado: [[gate-remoto-help-lanza-un-gate-y-un-fichero-sin-trackear-lo-bloquea]] · [[facturaia]]
