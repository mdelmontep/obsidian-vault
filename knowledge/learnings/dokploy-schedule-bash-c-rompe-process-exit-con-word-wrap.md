---
title: dokploy schedules — word-wrap rompe comandos largos en bash -c
date: 2026-05-02
source: claude-code-session
tags: [dokploy, infra, gotcha]
---

La UI de Dokploy invoca `bash -c <Command>` en el contenedor. Comandos largos en el campo Command pueden quedar guardados con espacios fantasma en medio de literales — vimos `process.ex   it` por wrap visual del editor.

Reglas:
- **NO añadir `bash -c` manualmente al Command** (confirmado 2026-05-11). Dokploy ya lo envuelve desde el dropdown Shell. Doble wrap → `bash -c curl -X POST ...` interpreta `curl` como script y `-X` como `$1` → curl falla con args inválidos. Caso real FacturaIA: cron `cashflow-alerts` fallaba con "Command failed" hasta quitar `bash -c` del campo Command.
- Preferir `curl -H "x-service-key: ${VAR}"` corto a `node -e "fetch(...)"` largo. Dokploy expande `${VAR}` con las envs del servicio.
- Si necesitas JS por algún motivo, envuelve TODO el snippet en comillas simples (`node -e '...'`) y mantenlo corto. Comillas dobles dejan que la shell del contenedor toque cosas.
- Verifica el comando guardado releyendo en la UI tras Save.
- Si el comando da `OCI runtime exec failed: bash: not found`, la imagen es Alpine/distroless. Cambia a `sh` o usa `node -e` (Node 18+ trae `fetch` nativo).
