---
title: colima publica en *:puerto lo que un contenedor escucha en 0.0.0.0, y queda abierto a la wifi
date: 2026-09-22
source: facturaia
tags: [colima, lima, docker, supabase, seguridad, macos]
---

Con Colima el reenvío de puertos lo hace Lima por ssh y ata el lado del host a `*`, no a
`127.0.0.1`. Un `supabase start` deja Postgres (contraseña `postgres`), Studio (sin auth) y la API
accesibles desde cualquier equipo de la red. Con el cortafuegos de macOS apagado no hay nada más.

Medido el 22-sep en el Mac de CI de facturaia: `nc -z <ip-lan> 54522` abierto desde otro Mac.
Y el Mac principal está igual: `lsof -nP -iTCP -sTCP:LISTEN` → `ssh *:54522`, `ssh *:5433`.

Fix (global a la VM, se aplica al ARRANCARLA): `~/.colima/_lima/_config/override.yaml` con
`portForwards: [{guestIP: 0.0.0.0, guestIPMustBeZero: true, guestPortRange: [1,65535], hostIP: 127.0.0.1, hostPortRange: [1,65535]}]`
y `colima stop && colima start`. Verificar contra la IP de LAN, no contra localhost, y probar la
cara que debe fallar (sin override → abierto). Lo automatiza `scripts/ci/provision-runner-mac.sh`.
