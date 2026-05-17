---
title: docker compose up no recrea container si solo cambia el valor de una variable referenciada
date: 2026-05-17
source: claude-code-session
tags: [docker, dokploy, env, infra]
---

Si el `docker-compose.yml` referencia `- VAR=${VAR}` y solo cambia el valor de `VAR` en el `.env`, `docker compose up -d` lo trata como "sin cambios" y NO recrea el container. La env nueva queda en disco pero el proceso sigue con la vieja en memoria.

**Síntoma típico**: tras Deploy/Reload de Dokploy, `docker ps` muestra el container "Up N horas" (no recreado), y `docker exec X env | grep VAR` devuelve vacío o valor viejo, aunque `.env` esté correcto.

**Fix**:
```bash
cd /etc/dokploy/compose/<stack>/code
docker compose up -d --force-recreate <service>
```

O en paneles (Dokploy/Portainer): buscar botón "Recreate" o "Restart" del container, no solo "Deploy" o "Reload".

**Aplica a**: Docker Compose puro, Dokploy, Portainer, cualquier orquestador que use compose internamente.

Relacionado: [[dokploy-paste-compose-corruption]].
