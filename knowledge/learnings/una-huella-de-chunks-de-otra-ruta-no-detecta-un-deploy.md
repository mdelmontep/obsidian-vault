---
title: una huella de chunks de otra ruta no detecta un deploy que solo toca una página
date: 2026-08-31
source: facturaia
tags: [deploy, nextjs, dokploy, verificacion]
---
Para esperar a que entrara un deploy usé como sonda el md5 de los `/_next/static/chunks/*.js`
de `/login`. Nunca se movió, y concluí «no ha desplegado». Había desplegado hacía rato.

Next.js hashea los chunks **por contenido** con ids de módulo deterministas: un fix que solo
toca el calendario deja los chunks de `/login` byte a byte iguales. La sonda no era ruidosa,
era **ciega**: solo puede dar falsos negativos, y no hay forma de distinguirlos de un deploy
que no ha entrado.

Lo que sí lo dice: `dokploy-safe.sh "/api/compose.one?composeId=<id>"` → `deployments[]`, con
`description: "Commit: <sha>"` y `status`. Ojo a la trampa contraria, ya conocida: ese campo
puede quedarse **stale** y enseñar commits viejos. Hoy acertó porque enseñaba mi sha, que es
información *más nueva*, no más vieja — un `deployments[]` que enseña TU commit no puede estar
stale hacia adelante.

Regla: una sonda de deploy tiene que mirar algo que **tu cambio toca**, o preguntar al
desplegador. Ver [[dokploy-autodeploy-false-desfase-silencioso]].
