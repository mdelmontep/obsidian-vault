---
title: op item move usa --destination-vault, no --vault; "private" resuelve al vault personal real
date: 2026-08-04
source: claude-code-session
tags: [1password, cli, gotcha]
---
`op item move <item> --current-vault <origen> --vault <destino>` falla: `unknown flag: --vault`.
El flag correcto es `--destination-vault`.

Además, `--destination-vault "Private"` no busca un vault llamado "Private": resuelve al vault
personal real de la cuenta. En una cuenta business puede llamarse distinto (aquí, `Employee`) y
ese nombre no sale en el `--help`, solo en el resultado del comando.

Antes de dar por hecho dónde quedó un ítem tras un `move`, leer el campo `Vault:` de la salida,
no el nombre que se pasó en el flag.

Ver [[service-account-de-1password-exige-vault-explicito-en-item-get]]
