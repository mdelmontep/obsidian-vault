---
title: curl -sf trata un redirect 3xx como éxito — cron que reporta verde sin ejecutar nada
date: 2026-07-02
source: claude-code-session
tags: [curl, cron, bugs-silenciosos, middleware]
---
`curl -f` solo falla con HTTP >= 400. Sin `-L`, un 307/302 devuelve exit 0 con
body vacío: el cron "triunfa" sin que el endpoint se haya ejecutado jamás.
Caso real (FacturaIA, PR #649): el cron Dokploy llamaba al worker VeriFACTU con
`curl -sf -X POST .../api/verifactu/process -H "x-service-key: ..."`, pero la
ruta no estaba en el allowlist del middleware de sesión → 307 a /login ANTES
del handler → 0 ejecuciones en toda la historia, cron siempre verde.
Defensas: (1) al añadir un endpoint de cron/servicio, smoke del endpoint REAL
por HTTP (no solo el handler en tests) y verificar que deja rastro (fila en
cron_runs, no solo exit 0); (2) en el comando del cron, considerar
`--fail-with-body` + asertar el body esperado, o al menos `-w '%{http_code}'`;
(3) todo endpoint sin sesión nuevo → allowlist del middleware (inviolable ya
existente que aquí se saltó).
