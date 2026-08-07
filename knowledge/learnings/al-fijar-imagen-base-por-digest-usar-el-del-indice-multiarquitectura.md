---
title: al fijar imagen base por digest, usar el del índice multiarquitectura (y con fecha de caducidad)
date: 2026-08-07
source: claude-code-session — TuCRMIA, Dockerfile
tags: [docker, dokploy, seguridad, reproducibilidad]
---
`FROM node:24-alpine` sin digest = dos builds del mismo commit pueden dar imágenes
distintas; la etiqueta se reescribe con cada parche y nada lo delata.

**La trampa al fijarlo**: hay que usar el digest del ÍNDICE multiarquitectura
(`application/vnd.oci.image.index.v1+json`), no el de una plataforma. Fijar el de
`linux/arm64` construye bien en el Mac y rompe (o trae binarios equivocados) en el
Linux/amd64 del servidor. Sin Docker local se saca por HTTPS:

```
TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/node:pull" | jq -r .token)
curl -sI -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.oci.image.index.v1+json" \
  https://registry-1.docker.io/v2/library/node/manifests/24-alpine | grep -i docker-content-digest
```

**Y crea el problema contrario**: los parches de Alpine dejan de llegar. Hace falta un
check de frescura, pero por EDAD (30 días), no por «difiere de la etiqueta» — eso pasa
cada pocos días y sería rojo permanente. La fecha sale del blob de config de la imagen.

Relacionado: [[trinquete-baseline-bloquea-solo-lo-nuevo-patron-reusable]]
