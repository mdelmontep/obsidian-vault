---
title: defense-in-depth de scopes duplicado diverge si no se espeja al añadir uno
date: 2026-06-19
source: claude-code-session
tags: [oauth, mcp, facturaia, seguridad]
---
El MCP de TuFacturaIA valida el vocabulario de scopes en DOS sitios independientes (defense-in-depth): `src/lib/oauth/policy.ts` (`GRANTABLE_SCOPE`/`MCP_GRANTABLE_SCOPES` → well-known + registro DCR) y `src/lib/mcp/user-token.ts` (`VALID_SCOPE` → verifier del JWT). PR #409 añadió `conciliacion:read` SOLO al primero → el token se firmaba con ese scope pero el verifier lo rechazaba → `401 "user token carries an invalid or non-grantable scope"` → cliente OAuth en bucle "Authorization failed".

No se pueden unificar en una sola const (dependencia circular: `policy` importa `McpScope` de `user-token`). Patrón: una allowlist duplicada a propósito DEBE llevar un test que itere la lista canónica y verifique que el OTRO lado la acepta. Fix #427: espejar la regex + test que valida que el verifier acepta todo `MCP_GRANTABLE_SCOPES`.

Instancia concreta de la regla CLAUDE.md "shape compartido = grep todos los consumidores". Latente: solo revienta al primer cliente que pide el scope nuevo.
