---
title: un lockfile puede pinnar un paquete npm ya retirado del registro, y solo lo revela un build con caché limpia
date: 2026-08-04
source: tucrmia — despliegue automático parado 17 commits sin que nada lo dijera
tags: [npm, deploy, dokploy, ci, gotcha]
---

`package-lock.json` puede fijar una versión exacta de un paquete que el autor **retiró** del registro npm
después (caso: `flat-cache@6.1.24`). `npm ci` la busca por versión exacta y falla — pero solo en una
máquina cuya caché de npm/`node_modules` no la tenga ya. El resultado: **todo despliegue que reconstruya
desde cero (Docker, Dokploy, CI) falla desde ese commit**, mientras `npm run build`/`next build` en local
sigue funcionando indefinidamente porque nunca vuelve a bajar esa dependencia.

Aquí costó **17 commits de despliegue automático fallando en silencio** (con `autoDeploy` recién
arreglado y confiado) hasta diagnosticarlo, y solo se vio leyendo los **logs reales** del build
(`dokploy-safe.sh`, nunca `application.one` a secas — filtra secretos), no por hipótesis.

**Fix**: `npm cache clean --force && rm -rf node_modules package-lock.json && npm install` para
regenerar el lockfile con una versión publicada, y verificar con un `npm ci` limpio antes de dar el
arreglo por bueno.

**Señal para buscarlo antes**: si el despliegue automático lleva parado más de un par de commits, no
asumir que el último cambio es la causa — comparar el commit reportado en `/health` (o su equivalente)
contra `origin/main` ANTES de depurar el código.
