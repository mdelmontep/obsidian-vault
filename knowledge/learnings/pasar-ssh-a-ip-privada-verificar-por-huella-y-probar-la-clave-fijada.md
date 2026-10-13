---
title: pasar ssh a ip privada: verificar el host por huella y probar la clave nueva fijada
date: 2026-10-13
source: agentesia-dokploy (cierre del SSH público, AIAVPN)
tags: [ssh, vpn, wireguard, dokploy, 1password]
---
Al mover los Dokploy a la VPN (10.250.0.x), tres trampas medidas:

- **IP privada que nadie te ha dado**: no la adivines ni la aceptes a ciegas. `ssh-keyscan -p 5251 -t ed25519 <privada>` y compara su huella con la que `known_hosts` ya tiene para la pública (`ssh-keygen -F "[<publica>]:5251"`). Si coincide, es la misma máquina; añade esa línea a `known_hosts`. Así salieron simarro (.169) y Clínica Zen (.168). El patrón fue «mismo último octeto», pero lo que lo prueba es la huella.
- **`Host 10.250.0.*` no se aplica a los alias**: ssh compara contra lo que tecleas, no contra el `HostName`. Cada alias necesita su propio `User`/`Port`/`IdentityAgent`.
- **Falso positivo al probar una clave nueva**: `-o IdentitiesOnly=yes` SIN `IdentityFile` sigue ofreciendo `~/.ssh/id_*` por defecto. Dos hosts «entraban con la clave de 1Password» y era la `id_ed25519` antigua (`ssh -v` → `Server accepts key`). Fíjala: guarda la `.pub` y usa `-o IdentityFile=<clave>.pub -o IdentitiesOnly=yes` con el agente de 1Password.
- **WireGuard en Mac**: «Añadir túnel vacío» y pegar desde la web puede no dejar guardar. Limpiar el portapapeles a ASCII, escribirlo a un `.conf` con `chmod 600`, importarlo y borrarlo después funcionó.

Relacionado: [[vps-dokploy-de-una-tanda-comparten-password-root]] · [[docker-infra]]
