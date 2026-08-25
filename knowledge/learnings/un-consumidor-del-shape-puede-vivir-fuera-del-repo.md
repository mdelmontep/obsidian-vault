---
title: un consumidor de un shape compartido puede vivir fuera del repo (n8n desplegado)
date: 2026-08-25
source: elphis-psicologia
tags: [n8n, contratos, integraciones]
---
«Cambio en shape compartido = grep todos los consumidores» tiene un punto ciego: el grep
solo ve el repo, y un workflow de n8n desplegado consume el mismo shape sin dejar rastro
grepeable. Caso real (25-ago, Elphis Psicología): la web renombró los slugs de servicio
(`desarrollo-personal` murió, `terapia-individual-adultos`→`adultos`) y el whitelist del
nodo «Validar input» del adaptador de agenda siguió con la lista vieja — toda reserva con
slug real habría fallado con `invalid_service`, con la suite E2E en verde (usaba fixtures
con los slugs viejos: el fixture también era un consumidor desincronizado).
Fix en tres capas: (1) parchear el nodo vía API y dejarle comentario de PROCEDENCIA
(«fuente canónica: web/src/lib/services.ts — grep los dos lados antes de editar»);
(2) `CHECK` en la tabla que persiste el valor — la red que faltó; (3) whitelist documentado
en el README del adaptador, para que el drift sea al menos visible en un diff.
Al cambiar un shape: además del grep, repasar los consumidores DESPLEGADOS (workflows n8n,
agentes Retell, plantillas Meta) desde README/memoria — el grep no los ve.
