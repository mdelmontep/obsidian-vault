---
title: una tanda E2E sin comprobar que el servidor sigue vivo al final no es una medición
date: 2026-07-28
source: claude-code-session
tags: [e2e, playwright, testing, nextjs, metodo, facturaia]
---

Los rojos de un servidor caído son **indistinguibles** de los de un bug, y empujan justo a la
reacción equivocada: subir timeouts. En una sola sesión (TuFacturaIA, 2026-07-27) invalidaron
cuatro tandas:

- `next dev` murió tres veces a los ~14 min de tanda y se llevó 11 tests con
  `ERR_CONNECTION_REFUSED`. Con la máquina paginando (otras sesiones con `tsc`/`next build`,
  load 50-138) el kernel elige al servidor.
- Un `next start` lanzado como **tarea de fondo del harness** recibía SIGTERM a los ~40 min.
  Arrancarlo con `nohup … & disown` para que no cuelgue de la herramienta.
- Una tanda dio 3 rojos en specs que el cambio ni tocaba y otro con "This page couldn't load".

Reglas:
- Medir contra `npm run build` + `npm start`, nunca contra `next dev`. Además es más rápido.
- **Terminar cada tanda con un `curl` al servidor**; si no responde 200, la tanda se tira, no se
  interpreta: `npm run e2e:smoke > log; curl -o /dev/null -w "VIVO=%{http_code}" localhost:PORT/login >> log`.
- Máquina compartida con otras sesiones = medición contaminada. Comprobar `uptime` antes.

Ver [[pre-commit-hook-oom-con-dev-server]] · [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] · [[facturaia]]
