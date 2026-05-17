---
title: dokploy puede corromper líneas al pegar yaml en pestaña compose
date: 2026-05-17
source: claude-code-session
tags: [dokploy, docker, infra]
---

Al pegar el `docker-compose.yml` completo en la pestaña Compose para añadir una línea nueva (ej. `- APP_URL=${APP_URL}`), Dokploy puede duplicar una línea adyacente en lugar de insertar la nueva. Caso real: pegué YAML con `APP_URL=${APP_URL}` en línea 30; Dokploy regeneró el compose con `FACTURAIA_SERVICE_KEY=${FACTURAIA_SERVICE_KEY}` duplicada en línea 30 y la línea de `APP_URL` desapareció.

**Síntoma**: tras Save + Deploy, env nueva sigue vacía en `docker exec X env`, aunque la viste en el editor de la pestaña Compose.

**Verificación obligatoria tras cualquier Save en pestaña Compose**:
```bash
ssh -p PORT root@HOST "grep -nE 'VARNUEVA|VARQUEDEBERIASEGUIR' /etc/dokploy/compose/<stack>/code/docker-compose.yml"
```
Si la línea esperada no está o hay duplicados → reabrir pestaña, localizar, reescribir, Save + Deploy.

**No basta con confiar en el editor del panel**. Source of truth = archivo en disco regenerado por Dokploy.

Relacionado: [[docker-compose-env-not-recreate]].
