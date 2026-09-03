---
title: un smoke lanzado antes de que el autodeploy termine mide el código viejo, y escribe con él
date: 2026-09-03
source: facturaia
tags: [dokploy, deploy, smoke, prod]
---
Merge a main a las 00:16, deploy de Dokploy creado a las 00:17, smoke a las 00:19: los dos POST
que debían probar la idempotencia crearon dos filas más en prod, porque el contenedor que
respondía era el anterior. El smoke no falló ruidosamente: dio 200 con el código viejo.

Un smoke sobre un cambio recién mergeado no es válido hasta comprobar que el deployment de ESE
commit está `done`, y menos si escribe: cada petición contra la versión vieja deja datos que
luego hay que explicar. Comprobar antes con el wrapper que redacta el env (`compose.one` en
crudo vuelca todos los secretos de prod):
`DOKPLOY_API_KEY=… ~/.claude/bin/dokploy-safe.sh "/api/compose.one?composeId=<id>"` y mirar
`deployments[]` por título del commit y `status`. Primo de [[un-comando-de-reparacion-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja-y-te-felicita]]: allí el checkout, aquí el contenedor.

Ver [[facturaia]] · [[dokploy-panel-no-es-el-contenedor]]
