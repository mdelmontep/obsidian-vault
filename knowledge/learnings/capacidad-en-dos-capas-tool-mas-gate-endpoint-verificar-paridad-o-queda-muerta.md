---
title: capacidad en 2 capas (tool que anuncia + gate de endpoint que autoriza) — verificar paridad o la tool queda muerta (403)
date: 2026-07-14
source: claude-code-session facturaia
tags: [facturaia, mcp, auditoria, seguridad]
---

Cuando una capacidad vive en 2 capas —una que la ANUNCIA (tool MCP / registro / manifiesto) y otra que la AUTORIZA (gate del endpoint)— un desajuste hace la tool **muerta**: se ofrece al LLM pero siempre 403, aun con rol y scope correctos.

Caso real (TuFacturaIA, MCP wrapper sobre v1): `authorizeV1Access` rechaza toda escritura por user-token si la ruta NO declara `requireWrite`. 6 tools MCP (`editar_presupuesto`, `cancelar_presupuesto`, `marcar_presupuesto_aceptado/rechazado`, `eliminar_borrador_*`) apuntaban a rutas v1 sin `requireWrite` → 403 garantizado. El inventario del MCP en aislado las dio como "sanas" (tienen handler); SOLO el cruce tool↔endpoint lo detectó.

Fix: `requireWrite` en las rutas + **test de invariante** que parsea todas las rutas de escritura y exige `requireWrite` salvo una allowlist explícita (la frontera fiscal emitir/anular/convertir, api_key-only). Detecta drift en ambos sentidos.

Regla: capacidad en 2 capas → paridad como **test de invariante sobre el filesystem**, no revisión manual (mismo patrón que openapi drift-guard). Es el caso INVERSO de [[defensa-cableada-vs-codigo-muerto]] (gate sin consumidores). Ver también [[matriz-permisos-rol-aware-bd-mas-espejo-ts]] · [[openapi-spec-mantenido-a-mano-deriva-del-handler]] · [[acciones-irreversibles-no-tool-mcp-autonoma]].
