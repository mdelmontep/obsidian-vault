---
title: dep con binario nativo (sharp) en ruta API Next — import dinámico dentro de try/catch
date: 2026-07-14
source: FacturaIA — auto-orientación OCR (#888), revisión adversarial
tags: [nextjs, alpine, docker, sharp, deploy, facturaia]
---
Un `import sharp from 'sharp'` estático (top-level) en una route handler: si el
`.node` nativo no carga en el runtime (Alpine/musl, o no trazado en
`output:'standalone'`), falla el import del **módulo entero** → la ruta devuelve
500 en TODA petición. Los try/catch alrededor de las *operaciones* no protegen:
el import es lo que revienta. En OCR esto = todos los documentos a 500 → el
worker los reintenta → backlog infinito.

Fix: carga **dinámica** dentro de try/catch — `const sharp = (await
import('sharp')).default` — así un fallo de carga degrada a "sin preprocesado"
en vez de tumbar la ruta. Además `next.config` → `serverExternalPackages`
incluir la dep (que NO se bundlee y el binario viaje al standalone).

Local (macOS) SIEMPRE carga el binario darwin → typecheck/build/dev verdes NO
prueban nada. Verificar en el contenedor Alpine real (invocar el endpoint en
prod tras deploy). Ver [[alpine-docker-sin-bash-ni-curl-anadir-via-dockerfile-para-crons]].
