---
title: dokploy schedules — word-wrap rompe comandos largos en bash -c
date: 2026-05-02
source: claude-code-session
tags: [dokploy, infra, gotcha]
---

La UI de Dokploy invoca `bash -c <Command>` en el contenedor. Comandos largos en el campo Command pueden quedar guardados con espacios fantasma en medio de literales — vimos `process.ex   it` por wrap visual del editor.

Reglas:
- Preferir `curl -H "x-service-key: ${VAR}"` corto a `node -e "fetch(...)"` largo. Dokploy expande `${VAR}` con las envs del servicio.
- Si necesitas JS por algún motivo, envuelve TODO el snippet en comillas simples (`node -e '...'`) y mantenlo corto. Comillas dobles dejan que la shell del contenedor toque cosas.
- Verifica el comando guardado releyendo en la UI tras Save.
- Si el comando da `OCI runtime exec failed: bash: not found`, la imagen es Alpine/distroless. Cambia a `sh` o usa `node -e` (Node 18+ trae `fetch` nativo).
