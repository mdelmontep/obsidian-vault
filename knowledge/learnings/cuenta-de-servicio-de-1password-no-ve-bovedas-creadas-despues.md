---
title: una cuenta de servicio de 1password no ve bóvedas creadas después de ella
date: 2026-09-05
source: mandadm
tags: [1password, opsa, secretos, cli]
---
El alcance de bóvedas de una cuenta de servicio se fija al crearla y **no se puede ampliar**
(documentación oficial; medido el 5-sep con la bóveda `MandaDM`): `op vault user grant --user <id>`
devuelve 400 y `op user list` ni siquiera lista cuentas de servicio. Salidas reales, de menor a mayor:
- Poner el ítem en una bóveda que la cuenta ya vea (`Compartida Agentesia`).
- Recrear la cuenta de servicio con las bóvedas nuevas (lo que se hizo: cuenta `Claude`, 18 bóvedas),
  cambiar el token del Keychain y `OPSA_TOKEN_EXPIRES` en `~/.local/bin/opsa`.
Al crear una bóveda nueva para un proyecto, asumir de entrada que `opsa` no la verá.
Gotcha al pegar el token nuevo → [[security-add-generic-password-interactivo-trunca-el-secreto-a-128]].
