---
title: ssh -i no aísla la clave, ofrece también la del config y la del agente
date: 2026-10-17
source: agentesia-skills (auditoría de gates_ed25519 tras el encierro de la Pizarra)
tags: [ssh, seguridad, 1password]
---
Para saber en qué servidores está autorizada una clave, `ssh -i clave -o IdentitiesOnly=yes host` miente: `-i` AÑADE la clave, no sustituye. ssh sigue ofreciendo el `IdentityFile` del `Host` en `~/.ssh/config` y lo que tenga el agente (1Password), y entra con esas.

Caso real (17-oct): la clave de gates «entraba» en 7 VPS; aislada, solo en gates.

Probar una clave sola: `-F /dev/null` (ignora el config) + `-o IdentityAgent=none` + `-o IdentitiesOnly=yes -i clave -o BatchMode=yes`. Usuario, host y puerto se sacan antes con `ssh -G <host>`.
Ver [[sandbox-exec-filtra-red-por-puerto-y-deja-llavero-y-env-abiertos]].
