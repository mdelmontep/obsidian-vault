---
title: agente ssh de 1password por terminal pide huella en cada comando de claude code
date: 2026-10-13
updated: 2026-10-16
source: claude-harness (sesión SSH vía 1Password, Mac; ~/bin/gate-remoto y VM gates, 15-oct-2026)
tags: [1password, ssh, claude-code, gates, gate-remoto]
---
- **Huella en cada `ssh` de Claude Code**: cada llamada a Bash es una shell nueva. Si se aprueba por *application and terminal session*, cada llamada cuenta como terminal nueva. Fix en Settings → Developer → SSH Agent: aprobar por **application**, recordar la aprobación un tiempo fijo y marcar la casilla «Approve for all applications». La aprobación solo se puede dar en el Mac; el móvil no sirve.
- **Pre-push o gate en segundo plano: `agent refused operation` → `Permission denied (publickey)`** (15-oct). Con 1Password autobloqueado, el agente no tiene la clave privada y pide desbloqueo en cada firma. En segundo plano nadie lo atiende. La aprobación sobrevive al bloqueo, pero la firma no. Ningún ajuste de aprobación lo arregla. El rechazo va por conexión: un script con 8 conexiones tiene 8 ocasiones de caer. La pista fue `lastUnlock` en `settings.json`, que coincidía al segundo con el fallo.
- **Fix para una máquina de builds**: clave dedicada en fichero y `IdentityAgent none` en su `Host`. En la VM, `restrict,pty,from=<subred de clientes VPN>`. En el script, un solo `ControlMaster` por corrida.
- **`from=` va con la subred de CLIENTES de AIAVPN (10.251.0.x)**, no con la de servidores (10.250.0.x). Si está mal, la clave buena sale con el mismo `Permission denied` que una ajena.
- **Para probar una sola clave**: `ssh -F /dev/null -i clave -p PUERTO user@IP`. `-i` añade la clave a las del `Host`, no las sustituye.
- **Coste aceptado**: cualquier proceso del usuario entra en la VM sin preguntar. Una passphrase en el Keychain no lo evita, porque ssh la lee sin preguntar. Vale si en la VM no hay sudo, Docker rootless y sin secretos.
- **«Pseudo-terminal will not be allocated»** sale con `RequestTTY auto`, sin orden remota y con stdin que no es una terminal; hasta `ssh -G` lo imprime. No viene del `pty` del servidor.
- Fuente: https://developer.1password.com/docs/ssh/agent/security · Relacionado: [[1password]]
