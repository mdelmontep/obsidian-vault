---
title: dockerfile copy con lista blanca crash-loopea al añadir módulos
date: 2026-08-14
source: claude-code-session
tags: [docker, deploy, runner]
---

Un `COPY a.mjs b.mjs c.mjs ./` enumerado a mano se desincroniza en cuanto otro PR
añade un módulo que el entrypoint importa: la imagen construye bien, el proceso
muere al arrancar (`ERR_MODULE_NOT_FOUND`) y el `restart: unless-stopped` lo
convierte en crash-loop infinito. Doble trampa: los reinicios del contenedor son
invisibles para la salud a nivel de aplicación (mide trabajo hecho, no arranques),
así que puede durar días.

Fix: `COPY *.mjs ./` (glob) — un módulo nuevo sube sin tocar el Dockerfile.
Caso real: marketing-runner de TuFacturaIA, 37 h y 76 reinicios (PR #1763).
Mismo espíritu que [[los-buckets-de-storage-se-crean-en-el-panel-y-no-viajan-con-el-repo]]:
toda lista manual que espeja otra cosa acaba mintiendo.
