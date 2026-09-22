---
title: hooks de Stop que bloquean minutos, y la tabla de routing de facturaia que pesa 5k tokens
date: 2026-09-22
source: claude-code
tags: [claude-code, hooks, harness, facturaia, contexto]
---

Datos del `/doctor` del 22-sep (50 sesiones, 5 días). Se midieron, pero no se ha arreglado nada.

- **`worktree-guard.sh` (Stop)**: se cortó por timeout en 4 de 4 ejecuciones, con una mediana de ~1.124 s. Bloquea el final de la respuesta. Es lo primero que hay que diagnosticar.
- **`stop-gate.sh` (Stop)**: mediana de 0,9 s y pico de 245 s.
- **`afplay … &` (Stop)**: mediana de 15 s. Hipótesis sin verificar: el proceso en background hereda stdout y el hook espera. Probar con `>/dev/null 2>&1 &` o con `"async": true`.
- **`claude-time-hook.mjs`**: está en `PostToolUse` sin matcher, así que arranca Node en frío tras cada herramienta. Como solo registra, es candidato a `async`.
- **facturaia `CLAUDE.md`**: la tabla de routing ocupa ~5,3k tokens (el 62 % del fichero). Siete filas pasan de 800 caracteres (albaranes 2,4k, huella fiscal, MCP, errores, marketing, agéntica). Se pueden reducir a disparador → fichero + regla dura (~2k de ahorro), pero hay que comprobar fila a fila que el ADR de destino ya contiene lo que se quita.

Relacionado: [[el-stop-gate-corre-el-gate-contra-la-base-compartida-y-un-temporal-sin-trackear-lo-dispara]]
