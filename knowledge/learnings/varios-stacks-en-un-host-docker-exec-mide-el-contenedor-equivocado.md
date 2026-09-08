---
title: con varios stacks en un host, docker exec te da la version del proyecto equivocado
date: 2026-09-08
source: centro-elphis
tags: [docker, dokploy, n8n, verificacion]
---

Un subagente afirmó "n8n es 2.36.5, no 2.20.9" con evidencia aparente: había leído el
`openapi.yml` de un contenedor. Era el de OTRO cliente del mismo servidor
(`elphispsicologia-n8nstack-kb7vtc`, imagen `n8nio/n8n:2.36.5`); el nuestro era
`elphis-n8nwithpostgres-wtqddl` con `n8nio/n8n:latest`, que responde 2.20.9.

Con Dokploy alojando varios proyectos, `docker ps | grep n8n` devuelve varios candidatos y
`docker exec $(docker ps | grep -m1 n8n)` coge el primero, que no tiene por qué ser el tuyo.
La afirmación resultante es falsa pero suena verificada, y contamina todo lo que se derive
de ella (qué acepta el PUT de la API, qué hace el sandbox).

Regla: el nombre del contenedor va **completo y literal** en el comando, nunca por `grep -m1`
ni por sufijo. Y una versión leída del host se contrasta con la que responde la propia API
del servicio. Ver [[dokploy-env-compose-section-necesaria-para-variables-custom]].
