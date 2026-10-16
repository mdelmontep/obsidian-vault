---
title: localhost en un ci con dockerd compartido puede contestar otro contenedor por ipv6
date: 2026-10-16
source: agh-iberica #2582 (VM gates, diagnóstico de Dani)
tags: [ci, docker, node, ipv6, gotcha]
---
Síntoma: una sonda `fetch("http://localhost:<puerto de docker port>")` recibe HTML de otra app. Sale verde con la VM vacía y roja cuando otros jobs corren a la vez.

- Node resuelve `localhost` primero a `::1` si `/etc/hosts` trae las dos.
- Un dockerd con `"ip": "127.0.0.1"` publica `-p 0:3000` solo en IPv4.
- Otros contenedores del mismo dockerd que publican en todas las interfaces (`services:` de Actions, Supabase) cogen puertos efímeros en `[::]` con un contador APARTE del de IPv4. Si `[::]:P` es de otro, la sonda le habla a ese.

Fix: sondear con `127.0.0.1`, nunca con `localhost`, cuando el puerto sale de `docker port` en un host compartido. No desactivar IPv6 en el dockerd: afecta a los demás repos.
Certeza: el mecanismo se vio en la VM, pero el choque no se reprodujo.

Relacionado: [[varios-runners-en-el-mismo-dockerd-chocan-por-nombre-de-proyecto-y-limpieza-global]] · [[puerto-3000-puede-servir-otro-proyecto-verifica-el-title]]
