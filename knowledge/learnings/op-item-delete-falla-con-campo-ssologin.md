---
title: op item delete falla en items con campo ssoLogin (login vía Google) — hay que borrar el campo antes
date: 2026-07-24
source: claude-code-session
tags: [1password, cli, bug]
---
`op item delete <id>` falla con `validateVaultItem failed: unsupported field type: ssoLogin` en cualquier item LOGIN que tenga un campo de tipo `ssoLogin` (los que el navegador guarda como "Inicia sesión con Google" — aparecen como `"type": "UNKNOWN"` en el JSON de `op item get`). Parece que delete revalida el item completo contra un schema que no reconoce ese fieldType.

Fix: antes de borrar, quitar el campo con `op item edit <id> 'NombreSección.NombreCampo[delete]'` (escapando puntos literales del nombre de sección con `\.` si los tiene, ej. `dashboard\.ngrok\.com`). Tras editar (sube de versión), el delete funciona normal.

No confundir con expiración de sesión (`authorization timeout`) — el mensaje de error es idéntico en texto pero la causa es otra; si el edit+delete falla igual tras reintentar, sí es sesión.
