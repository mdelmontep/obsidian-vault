---
title: slack canvas api no permite leer contenido de secciones
date: 2026-04-24
source: claude-code-session
tags: [slack, api, canvas]
---

`canvases.sections.lookup` devuelve metadata de secciones (titulo, ID) pero NO el contenido markdown dentro de ellas. No hay endpoint publico en la Slack API (2026-04) para leer el cuerpo de un canvas.

## Implicacion

- Para "editar una seccion especifica" no puedes leer lo que hay — solo append con `insert_at_end` o `insert_after_section`
- Si necesitas el contenido actual, la unica opcion es que el usuario lo copie manualmente o usar `files:read` para descargar el canvas como archivo (limitado)
- Disenar integraciones con canvas asumiendo write-only: append nuevo contenido, nunca modificar existente

## Scopes necesarios

Para editar canvas en canales privados: `canvases:write` + `channels:join` + `groups:history` + `files:read`
