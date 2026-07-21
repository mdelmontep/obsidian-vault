---
title: blueprint clonado trae Ollama sin usar — 11GB de disco muertos, no aparecía en el volumen persistente
date: 2026-07-21
source: claude-code-session
tags: [dokploy, docker, disco, ollama, blueprint]
---

Caso Clínica Zen: disco al 90%. El stack se desplegó desde una plantilla genérica
"n8n + postgres + ollama" (nombre del compose literal:
`*-n8nrunnerpostgresollama-*`), pero el chatbot real del cliente usa OpenAI
(GPT-5.1) — ningún workflow ni credencial documentada usa Ollama. Antes de asumir
"hay que ampliar disco", `docker system df -v` mostró:

- Imagen `ollama/ollama`: 6.17GB
- Capa escribible del contenedor con un modelo ya descargado: 5.0GB dentro de
  `/root/.ollama` — **NO** en el volumen Docker persistente (`ollama_storage`,
  que por eso seguía viéndose "vacío" en cualquier inventario de volúmenes:
  4.0K). Es decir, ni siquiera sobreviviría a una recreación del contenedor.

Fix: `docker stop` + `docker rm` del contenedor + `docker rmi` de la imagen →
11GB recuperados sin tocar nada en uso real.

Gotcha relacionado: las imágenes `<none>` (dangling) que aparecen en
`docker system df -v` **no son automáticamente basura**. En el mismo diagnóstico,
3 imágenes `<none>` (dokploy, postgres, redis, ~3.47GB) resultaron ser las
imágenes EN USO real por los contenedores vivos de Dokploy/su Postgres/su Redis
—solo aparecían como `<none>` porque el tag rotó a una versión más nueva en el
registry, pero el contenedor en marcha sigue corriendo sobre el ID viejo. Docker
lo protege solo (`docker rmi` da "cannot be forced — image is being used by
running container X") — si da ese error, es la señal de que NO hay que insistir
ni forzar el borrado, no un bug a resolver.

Mismo patrón que [[supabase-selfhosted-realtime-roto-slot-replicacion-crece-wal-sin-limite]]:
piezas de una plantilla clonada que nunca se llegaron a usar por el cliente real,
descubiertas auditando disco antes de escalar infra.
