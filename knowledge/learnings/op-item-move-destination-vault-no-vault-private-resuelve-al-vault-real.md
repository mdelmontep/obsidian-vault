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

**Y `move` no cruza cuentas** (31-ago): si el origen está en `my.1password.com` y el destino en la
cuenta de empresa, el comando no ofrece el vault y no hay flag que lo salve — hay que crear el ítem
nuevo en el destino y borrar el viejo, con lo que **el ID cambia igual**. Antes de planear nada:
`op account list`. En esta máquina devuelve **«No accounts configured for use with 1Password CLI»**,
o sea que `op` no es que pida huella: no tiene ninguna cuenta dada de alta, y hasta activar la
integración con la app de escritorio la terminal no es camino para NINGÚN `op`. Solo va `opsa`.

Ver [[service-account-de-1password-exige-vault-explicito-en-item-get]]
