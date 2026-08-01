---
title: si el proxy ya gatea la ruta, el gate de rol del handler es código muerto (y rompe al cliente)
date: 2026-08-01
source: claude-code-session facturaia
tags: [auth, middleware, nextjs, seguridad, api]
---
Dos rutas bajo `/api/admin/*` pedían `propietario|admin` en vez de superadmin. Lo clasifiqué como «rompe la invariante pero no hay fuga: operan contra la org del caller». **Faltaba la mitad**: el proxy ya gateaba `/api/admin/*` por superadmin y redirigía al resto a `/dashboard`, así que ese `requireRole` **nunca llegaba a ejecutarse**.

No es cosmético, es un fallo funcional y silencioso: el cliente recibe un **307**, `fetch` sigue el redirect y `res.json()` revienta con el HTML del dashboard. El panel llevaba roto para todos los clientes, e invisible porque quien lo probaba era superadmin, y para él el proxy sí pasa.

Reglas:
- Una ruta cuya auth REAL no coincide con la del prefijo que la contiene está mal colocada. Muévela a un prefijo cuya auth sea la suya; no documentes la excepción, porque la excepción no funciona.
- Al auditar auth por prefijo, mira los DOS planos (proxy y handler) y quién gana. Un grep de «¿todas piden superadmin?» da falso verde justo en las que están rotas.
- Prueba el camino con la cuenta del **público real** de la pantalla, no con la tuya de superadmin: el privilegio de más esconde exactamente esta clase de fallo.

Ver [[defensa-cableada-vs-codigo-muerto]] · [[helper-de-auth-que-asume-validacion-del-caller]]
