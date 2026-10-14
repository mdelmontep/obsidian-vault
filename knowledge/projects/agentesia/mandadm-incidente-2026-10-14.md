---
title: MandaDM comprometido por React2Shell en dokploymanu (incidente 14-oct-2026)
date: 2026-10-14
source: AgentesIA-MAdrid/mandadm (host dokploymanu, 185.99.186.76)
tags: [incidents, postmortem, seguridad, mandadm, nextjs, react2shell, docker, dokploy, minero]
---

# MandaDM comprometido por React2Shell (14-oct-2026)

Proyecto: [[mandadm|MandaDM]]. Host: Dokploy `dokploymanu` (185.99.186.76), el mismo que [[aula|Aula]].
Log: [[incidents]]. Sin secretos en esta nota.

## Superficie

- Contenedor `mandadm-web-1`, imagen `mandadm-app:latest`: **Next 15.1.6 + React 19.0.0**, arrancado el 10-sep-2026.
- Corría como **root**: el Dockerfile no tenía `USER`.
- Entrada: **React2Shell** (CVE-2025-55182 / GHSA-9qr9-h5gf-34mp), RCE en React Server Components. Había exploit masivo desde dic-2025.

## Cronología (dentro del contenedor, varios actores)

| Fecha | Hecho |
|---|---|
| 10-sep | Arranque del contenedor con la imagen vulnerable |
| 11-sep | `docker.io` instalado; `authorized_keys` con claves `root@36fcf52b51e9` |
| 12-sep | XMRig en `/root/sysl` |
| 16-sep | Segundo minero en `/root/.cache/.cache_t0` + vigilante `/root/.local/share/.cache_9/wd_` |
| 17-sep | gsocket (THC) como `/usr/local/bin/terminate-engine`, disfrazado de `-bash`; usuario `pakchoi` con uid 0; unidad que descarga de 195.178.110.29; temporizador `docker start amco_00c7f5db` (falló: no había `docker.sock`) |
| 14-oct 01:45 | **Detección**: el build Dokploy del CRM ([[tucrmia|TuCRMIA]], `tucrmia-web`) muere por OOM; el OOM killer mata un falso `redis-server` de 2,4 GB del contenedor de MandaDM. El CRM se queda en el commit `41537a8` (3-sep) en vez de `543873bc` |
| 14-oct ~13:25 | **Contención** |

Hashes: `terminate-engine` df6a1c28…f725bf · `terminate-runner` f6de3424…0f1126.

## Contención

- Pruebas en `/root/ir-20261014` del host (`docker export`, 475 MB).
- `docker stop` + `restart=no` de `mandadm-web-1`.
- Contenedor no privilegiado, sin montajes ni `docker.sock`. Barrido de los otros 30 contenedores y del host: sin indicios.

## Alcance asumido

- Todos los secretos de env de MandaDM, leídos.
- La base Supabase autohospedada de MandaDM (mismo host y misma red), leída.
- Tokens de Instagram del cliente tester, comprometidos.
- **Pendiente**: verificar la contraseña del Postgres interno de Dokploy (en `dokploy-network`).

## Remedio

- PR mandadm#2: next 15.5.27, react 19.0.8, `USER node`, `npm ci`. Gate en VM 713/713.
- **Pendiente de Manuel**: rotación de secretos y reconexión de las cuentas de Instagram.
- Auditoría del resto de repos: Aula (`learn-agentesia`, mismo host, next 16.2.11) y `tufacturaia-web` (next 16.2.6) con críticos; PR en curso.

## Lecciones

1. **Todo Next con RSC se parchea en días, no semanas.** El exploit masivo existía desde dic-2025 y la imagen llevaba 15.1.6 en sep-2026.
2. **Imágenes siempre con `USER` no root.**
3. **El minero se detectó solo por un OOM ajeno.** Falta alerta de CPU/RAM por contenedor en los Dokploy.
4. **El modo automático de Claude bloquea las lecturas de producción.** La respuesta a incidentes pasa por scripts que Manuel lanza con `!`.

Relacionado: [[docker-infra]] · [[supabase-selfhosted-cuatro-contenedores-y-seis-errores-enganosos]]

## Dokploy del host: secreto de sesión público (14-oct, 15:05)

- `comprobar-dokploy-db.sh tucrmia`: Dokploy v0.30.6 **sin** `BETTER_AUTH_SECRET(_FILE)` → firmaba sesiones con el default público `better-auth-secret-123456789` (GHSA-w3gm-rc4p-9rhj, admin del panel → root en el host). Actualizar de versión NO lo arregla.
- Arreglado con el script oficial `https://dokploy.com/security/0.29.3.sh` (sha256 `bee595fb…2815`): secreto `dokploy-auth-secret`, servicio convergido, sesiones invalidadas, 0 registros 2FA. Verificado: `BETTER_AUTH_SECRET_FILE` presente.
- Postgres interno de Dokploy correcto (docker secret, login por defecto rechazado, sin puerto publicado).
- Pendiente: revisar Users/API keys del panel por altas ajenas; repetir la comprobación en el resto de Dokploy (requiere VPN AIAVPN).
- Auditoría del panel (17:13, `auditar-panel-dokploy.sh`): solo 2 usuarios (Daniel owner, Manuel admin), 1 invitación aceptada, 3 API keys (Notcaido, trade, CRM), 0 2FA, 7 schedules de facturaia creados en abr-may, 37 sesiones todas desde IPs residenciales/móviles españolas y 147.96.x (UCM); ninguna sesión entre el 10-sep y el 14-oct. Sin contenedores ni servicios ajenos. **Sin indicios de entrada por el panel.**
- 17:26: secreto propio aplicado también en agentesia, agh, clinicazen, simarro, tufacturaia y elphis (los seis estaban sin `BETTER_AUTH_SECRET_FILE`, incluso v0.30.7). Verificado `BETTER_AUTH_SECRET_FILE: 1` en todos.
- 17:44: auditoría de los seis paneles. Usuarios solo del equipo; sesiones desde IPs españolas conocidas, 185.99.186.68 (Dani, abril) y scripts propios (curl/python de Manuel en agentesia, 13-14 oct). Única alta posterior al 10-sep: `birisarrio@agentesialabs.com` en agentesia (invitado por Borja el 21-sep como member, hoy admin): confirmar con Borja. Sin schedules ni contenedores ajenos. **Sin indicios de entrada por ningún panel.**
- clinicazen y simarro: el pooler de Supabase publica 0.0.0.0:5432; IPv4 cortado por `DOCKER-USER -i eth0 ... DROP`; IPv6 pendiente de comprobar (`comprobar-pooler-5432.sh`).
