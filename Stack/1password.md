---
title: 1Password CLI — opsa (service account) y cuándo usar op
date: 2026-09-28
source: claude-code-global
tags: [1password, opsa, secretos, cli]
---

# 1Password: `opsa`, nunca `op`, para LEER

Movido desde `~/.claude/CLAUDE.md` §Herramientas CLI (28-sep-2026). El global conserva la regla; aquí el alcance y los gotchas.

- **Lectura**: `opsa read "op://<vault>/<item>/<field>"`. `opsa` usa el service account con el token en Keychain: sin Touch ID, sin sesión.
- **Por qué no `op`**: `op` a secas pide huella que la shell del agente no puede pintar (cuelgue de 60 s / «account is not signed in»). El hook `~/.claude/hooks/op-guard.sh` lo bloquea y remite a `opsa`.
- **Alcance**: cuenta de servicio **Claude** (creada 5-sep-2026; sustituye a claude-code-mac). 18 bóvedas de `agentesialab.1password.eu`, incluida MandaDM, con permiso de **lectura y escritura** (la anterior era solo lectura: seguir usándola solo para leer).
- **Caducidad del token**: ver `OPSA_TOKEN_EXPIRES` en `~/.local/bin/opsa` (no copiar la fecha aquí: caduca la nota, no el fichero).
- **`opsa item get` exige `--vault` explícito** aunque busques por ID (sin él: «isn't an item»). `item list` y `read "op://vault/..."` no lo necesitan.
- **Fuera de alcance**: `my.1password.com` y los vaults `Private`/`Employee`/`Shared`. Ahí: `op` con huella, o mover el ítem a `Compartida Agentesia`.
- **Escritura**: `opsa item create --vault <b> --template <f.json>` (medido 10-sep creando el ítem del stack de mandadm). Con `--template` el secreto va en fichero, no en `argv`: borrarlo después.
- **Higiene**: NUNCA imprimir el secreto; consumir inline (`PGPASSWORD=$(opsa read ...) psql ...`). Tampoco en args de permisos ni en settings: un secreto pegado en `settings.local.json` queda en disco en claro.

- **Agente SSH**: si pide huella en cada comando de Claude Code → [[agente-ssh-de-1password-por-terminal-pide-huella-en-cada-comando-de-claude-code]].
- **Crear claves SSH o tocar authorized_keys** → guion `/wizard` desde el primer paso (huella de 1Password, VPN, prueba de la clave fijada). Ver [[pasar-ssh-a-ip-privada-verificar-por-huella-y-probar-la-clave-fijada]].

Ver [[op-item-delete-falla-con-campo-ssologin]] · [[op-cli-instalar-arm64-sin-homebrew]] · `Stack/claude-code-gotchas.md` (arqueología pre-service-account).
