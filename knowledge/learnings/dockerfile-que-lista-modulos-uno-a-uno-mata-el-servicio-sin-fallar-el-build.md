---
title: un dockerfile que lista los módulos uno a uno mata el servicio sin fallar el build
date: 2026-08-03
source: claude-code-session
tags: [docker, deploy, runner, facturaia]
---

El Dockerfile del ticket-runner copiaba sus `.mjs` **enumerados**:
`COPY run-ticket.mjs`, `COPY claude-accounts.mjs`… Añadí `reconciliar-prs.mjs` al
repo y no a esa lista. Consecuencias, en orden de maldad:

1. **El build NO falla.** La imagen se construye perfecta y se despliega.
2. El contenedor arranca, el `import` revienta con `Cannot find module` y el
   proceso muere. Nadie mira ese log.
3. El síntoma que sí se ve apunta a otro sitio: los jobs mueren 60 min después
   con *«nadie reclamó el job — runner caído o pausado»*, que suena a Dokploy, a
   cuota agotada o al kill-switch. Se perdieron dos tickets de cliente antes de
   que nadie abriera el Dockerfile.

Arreglo: `COPY *.mjs ./` (el glob no es recursivo, así que `__tests__/` no
entra). Y un test que compara los `.mjs` del directorio con lo que el Dockerfile
copia — el fallo no fue escribir código, fue **empaquetarlo**, así que el guard
va sobre el Dockerfile y no sobre el import.

Regla general: si un `COPY` enumera ficheros que un `import` resuelve en runtime,
tienes una lista que hay que recordar actualizar y ningún gate que lo verifique.

Ver [[autodeploy-sin-watchpaths-mata-el-trabajo-en-vuelo-del-worker]] ·
[[el-parte-de-un-job-caido-no-es-evidencia-de-lo-que-dejo]]
