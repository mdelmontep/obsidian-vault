---
title: en dokploy «rebuild» no recrea el contenedor, y el sello de build no ve un reinicio
date: 2026-08-26
source: agh-iberica
tags: [dokploy, docker, deploy, observabilidad]
---
Tras cambiar una env en el panel de Dokploy, pulsar **`Rebuild` no aplica nada**: construye la imagen
y deja el contenedor vivo con el env viejo. Solo **`Deploy`** clona y recrea. Los dos terminan en
`Done` verde ⇒ **el panel no discrimina**: hay que abrir el log del deployment.
- `Rebuild`: duración `0s`, todos los pasos `CACHED`, **sin `git clone`**, acaba en `✅ Docker build completed.`
- `Deploy`: trae `Receiving objects…` y el commit.

Y el corolario que cuesta más caro: **un sello de build (`/version` → `builtAt`) es CIEGO a un
reinicio**. Lo escribe un `RUN` del Dockerfile, vive en una capa **cacheada** y por construcción no se
mueve aunque el proceso rearranque. Responde «¿qué contenido corre?», nunca «¿rearrancó?». Estuve
~15 min haciendo polling de un valor que no podía cambiar. La señal buena es la pestaña **Logs**:
`Up N minutes` + la línea de arranque con hora, o `docker inspect --format '{{.State.StartedAt}}'`.

Ver [[una-ventana-de-observacion-anclada-al-arranque-caduca-con-cada-merge]] · [[un-comentario-no-puede-afirmar-el-estado-de-un-panel-de-deploy]]
