---
title: docker volume prune no toca los volúmenes con nombre, y al purgar se pierde quién los creó
date: 2026-08-18
source: claude-code-session limpieza-mac
tags: [docker, colima, disco, postgres]
---

Dos cosas que se descubren tarde y caras:

**1. `docker volume prune` solo borra los ANÓNIMOS.** Los que tienen nombre
sobreviven y siguen contando como huérfanos. Tras purgar 203 volúmenes (22,75 GB)
quedó uno vivo (`supabase_edge_runtime_*`, 40 MB) que parecía haberse ido. Para
esos hace falta `prune -a` o un `rm` explícito, mirando uno a uno: son datos.

**2. Al purgar se destruye la evidencia de quién los creaba.** Un volumen no tiene
campo `CreatedBy`: la relación con su contenedor vivía en el `docker inspect` de ese
contenedor, y «huérfano» significa justo que ya no existe. Tras el prune no queda ni
fecha ni tamaño, así que la fuga sigue abierta y sin culpable. **Antes de barrer:**

```bash
docker volume inspect $(docker volume ls -q) > ~/docker-volumes-$(date +%F).json
```

Lo que sobrevive en ese json: `CreatedAt`, las labels `com.docker.compose.*` (solo si
los creó compose; los de `docker run` llevan únicamente `com.docker.volume.anonymous`)
y el tamaño. Agrupar los anónimos por tamaño es la mejor pista del origen —203
clusters de Postgres de ~53 MB = el mismo proceso repetido— pero es heurística, no
prueba.

Radar read-only que lo enseña sin borrar: `~/.claude/bin/docker-radar`.
Ver [[colima-el-disco-sparse-no-encoge-al-borrar]].
