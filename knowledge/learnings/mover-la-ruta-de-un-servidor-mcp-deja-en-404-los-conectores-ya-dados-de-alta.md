---
title: mover la ruta de un servidor mcp deja en 404 los conectores ya dados de alta
date: 2026-09-24
source: facturaia
tags: [mcp, conectores, claude-ai, compatibilidad]
---
**Qué pasa:** el 9-sep (#2662) el MCP de TuFacturaIA pasó de `https://mcp.tufacturaia.com` a `…/mcp`. Todo conector de claude.ai dado de alta antes guarda la URL vieja y cae con `HTTP 404`. Claude Code muestra el error de la URL, no el cuerpo del 404, así que el `hint` con la ruta nueva no lo ve nadie.

**Cómo se detectó:** 15 días después, al intentar crear un presupuesto desde Simarro. Nadie lo había notado porque el conector solo se usa a ratos.

**Diagnóstico en 1 min:** `curl -X POST` a la raíz (404 + hint) y a `/mcp` (401 = vivo, falta OAuth); `/.well-known/oauth-protected-resource` en 200.

**Fix del usuario:** claude.ai → Settings → Connectors → quitar y volver a añadir con `/mcp`; luego `/mcp` → Reconnect (con la URL vieja sigue fallando hasta re-darlo de alta; el nombre del conector puede cambiar, p. ej. `FacturaIA` → `TuFacturaIA`).

**Patrón:** cambiar la ruta de un endpoint que terceros tienen registrado es un breaking change: seguir sirviendo la ruta vieja o avisar a quien lo tenga dado de alta. Un 404 con pista en el cuerpo no avisa a nadie.
