---
title: los VPS Dokploy de una misma tanda comparten la contraseña root
date: 2026-08-06
source: claude-code-session
tags: [dokploy, infra, ssh, 1password, credenciales]
---
Cuando "falta la clave SSH de un host X en 1Password" no hace falta buscarla ni resetear nada: **todos los Dokploy de Manu comparten la MISMA contraseña root**, no solo los de una tanda. Puerto SSH **5251** (el 22 cerrado) en todos. Confirmado en 5 hosts, incluso en proveedores distintos: tanda `185.47.13.x` (Clínica Zen `.168`, Simarro `.169`, tufacturaia `.170`, Elphis `.173`) **y** el Dokploy de Tecnocloud `dokploymanu` = `185.99.186.76` (host DOKPLOYMANU, donde corre TuCRMIA). La contraseña del ítem de Clínica Zen (`op://igr3mi3q3d3lg4dgcpiebim6oi/rnnqzte4pvqeq2ug767wyaulki/password`) abre todos. Ojo: la de "SSH Laserys" (mismo rango .186 que Tecnocloud) y la "dokploy root plantilla" **no** son la buena — probar directamente la de Clínica Zen.

Además esos hosts nunca tuvieron "clave SSH": se operaban por contraseña root. El acceso por clave se DOCUMENTA así (patrón replicado en los 4):
1. `ssh-keygen -t ed25519 -f ~/.ssh/<host>_root` (clave dedicada compartida).
2. Autorizar con la pass de la tanda: `export SSHPASS="$(opsa read 'op://<vault>/<item>/password')"; sshpass -e ssh -p 5251 root@<IP> '... append pubkey a authorized_keys (idempotente con grep -qxF) ...'`. Necesita `sshpass` (brew) — sin él `ssh-copy-id` pide prompt interactivo.
3. Guardar en 1Password con `op` (Touch ID → en Warp, no en Claude Code): documento con la privada + ítem SERVER (host/puerto/root/pass) clonando el de Clínica Zen.

Gotcha del harness: el **clasificador de Claude Code bloquea el SSH saliente a prod con root** aunque tengas la credencial → ese comando lo ejecuta el usuario con `!`. Instancia del patrón [[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]]. Ver también [[dokploy-api-docker-getcontainers-estado-sin-ssh]] · [[service-account-de-1password-exige-vault-explicito-en-item-get]].
