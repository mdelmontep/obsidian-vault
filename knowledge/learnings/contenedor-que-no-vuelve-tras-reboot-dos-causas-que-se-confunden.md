---
title: un contenedor que no vuelve tras el reboot tiene DOS causas distintas — no asumas la restart policy
date: 2026-08-07
source: claude-code-session
tags: [docker, dokploy, swarm, reboot, overlay, incidentes]
---

Tras reiniciar un host Dokploy, si faltan contenedores hay **dos causas diferentes** y se confunden porque el síntoma es idéntico (`Exited (143)`, no vuelve solo). Distinguirlas con `docker inspect`, no de memoria — yo di por buena la primera en un host donde la causa era la segunda.

**Causa A — restart policy `no`.** El stack se creó sin `restart:` en el compose, así que Docker no tiene ninguna instrucción de rearranque.
```bash
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' <container>   # -> no
```
Determinista: cae en **todos** los reboots. Arreglo en origen: añadir `restart: unless-stopped` a los servicios del compose desde el panel de Dokploy (editarlo solo en `/etc/dokploy/compose/<appName>/code/docker-compose.yml` se pierde en el siguiente deploy, porque Dokploy reescribe el fichero desde su BD). Parche inmediato hasta entonces: `docker update --restart unless-stopped <container>`.
Caso real: `simarro-documenso-wuclzk-{documenso,postgres}-1` en Simarro (185.47.13.169) — su compose no tiene ninguna línea `restart:`.

**Causa B — carrera con la overlay `dokploy-network`.** La policy es correcta (`unless-stopped`) y aun así no arranca. En Swarm, `dockerd` restaura los contenedores con restart policy **antes** de que Swarm haya reconstruido las redes overlay. El que llega antes muere:
```
failed to start swarm container ... error="failed to set up container networking:
could not find a network matching network mode dokploy-network: network dokploy-network not found"
```
y **no lo reintenta**. Se ve en `journalctl -b 0 -u docker | grep "$(docker inspect -f '{{.Id}}' <container>)"`.
No es determinista: es una carrera, y le puede tocar a **cualquiera** de los contenedores attachados a `dokploy-network` (los que Traefik enruta). En DOKPLOYMANU eran 5 candidatos y solo cayó uno.
Caso real: `web-agentesia-n8n-agentesia-djupl9-n8n-1` en DOKPLOYMANU (185.99.186.76) tras el reboot del 7-ago.

**El discriminador es una sola línea.** Si la policy es `no` → causa A. Si es `unless-stopped`/`always` y aun así no volvió → causa B, y lo confirma el journal del boot. Comparar también `StartedAt` con `uptime -s`: si el contenedor arrancó después del boot, lo levantó alguien a mano y no volvió solo.

Arreglo de la causa B: unidad systemd `oneshot` `After=docker.service` que espera a que `docker network inspect dokploy-network` responda y entonces arranca los contenedores parados cuya policy no sea `no` **y** cuyo `FinishedAt` sea anterior a `uptime -s` (esa segunda condición es la que evita resucitar algo que se paró a mano después de arrancar la máquina).

**Estado (7-ago-2026).** Instalado y `enabled` en DOKPLOYMANU: `/usr/local/bin/dokploy-restart-orphans.sh` + `/etc/systemd/system/dokploy-restart-orphans.service`, log en `/var/log/dokploy-restart-orphans/`. Simarro NO lo necesita: en su `dokploy-network` solo hay servicios de Swarm (los rearranca Swarm; por eso su policy es `no` y es correcto) — allí se arregló la causa A con `docker update --restart unless-stopped` sobre los dos documenso, pendiente de llevarlo al compose del panel para que sobreviva a un redeploy.

Cómo se validó, porque la corrida en seco no vale: con todo arriba el script dice "0 arrancados, 0 omitidos", que es indistinguible de un script roto. El arnés que sí discrimina usa un contenedor de juguete (`docker run -d --restart unless-stopped --name guardian-test alpine sleep 3600` + `docker stop`) y ejercita las dos ramas — tal cual da SKIP (murió después del boot), y con una copia en `/tmp` con `BOOT_EPOCH` falseado a `now` da START. Ambas verificadas.

Corolario del método: "no rearrancó por su restart policy" es una hipótesis, no un diagnóstico, hasta que `docker inspect` lo dice. Extrapolar la causa de un host a otro porque el síntoma coincide es exactamente el fallo. Ver [[verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado]] · [[dokploy-api-docker-getcontainers-estado-sin-ssh]] · [[vps-dokploy-de-una-tanda-comparten-password-root]].
