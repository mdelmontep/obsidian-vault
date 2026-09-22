---
title: hooks de Stop que bloquean minutos, y la tabla de routing de facturaia que pesa 5k tokens
date: 2026-09-22
source: claude-code
tags: [claude-code, hooks, harness, facturaia, contexto]
---

Datos del `/doctor` del 22-sep (50 sesiones, 5 días).

**Hooks: RESUELTO el mismo 22-sep** (`~/.claude` `d68cee8`, facturaia #2857):
- `worktree-guard`: los filtros van de más barato a más caro; baja de 12-16 s a 4,7 s y lleva `timeout: 60`.
- `afplay`: `>/dev/null 2>&1 &` + `async`. El `&` sin redirección retenía el pipe del hook.
- `claude-time-hook`: `async` solo en PostToolUse.
- Guards de Bash: extracción con jq y criba previa. Ver [[un-guard-caro-se-criba-con-la-condicion-necesaria-de-sus-reglas]].
- facturaia: eslint/stylelint con `--cache --cache-strategy content` (17 → 4 s).
- Descartados con medida: admitir por presión de memoria en fia-gate (faltan muestras), hardlink de `node_modules`, `NODE_COMPILE_CACHE` (~10 % de arranque) y subir `maxWorkers` (efecto menor que el ruido de carga).

**Sigue abierto:**
- **facturaia `CLAUDE.md`**: la tabla de routing ocupa ~5,3k tokens, el 62 % del fichero. Siete filas pasan de 800 caracteres (albaranes 2,4k, huella fiscal, MCP, errores, marketing, agéntica). Se pueden dejar en disparador → fichero + regla dura, con un ahorro de ~2k tokens. Antes hay que comprobar fila a fila que el ADR de destino ya contiene lo que se quita.
- **agency-portal**: 21 ramas con commits sin subir, respaldadas en `refs/backup/worktrees-2026-09-22/`, sin decidir si aportan algo a main. Las tres grandes son fase2-033, fase2-remediacion y sin-coverage.

Relacionado: [[el-stop-gate-corre-el-gate-contra-la-base-compartida-y-un-temporal-sin-trackear-lo-dispara]]
