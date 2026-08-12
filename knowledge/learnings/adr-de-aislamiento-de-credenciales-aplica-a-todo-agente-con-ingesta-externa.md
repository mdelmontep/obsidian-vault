---
title: adr de aislamiento de credenciales aplica a todo agente con ingesta externa
date: 2026-08-12
source: claude-code-session
tags: [seguridad, agentes, prompt-injection, adr]
---
Al migrar una fuente de datos de fichero a BD (12-ago, facturaia contenido-01), el paso
«actualiza la skill/agente para leer de BD» inyectó sin querer la conexión psql de prod
(superusuario) en los prompts persistentes del agente de marketing — que tiene WebSearch +
Bash. Eso recrea exactamente el vector que ADR-012 acababa de cerrar para el runner: un
prompt injection en texto externo se convierte en lectura de la BD multi-tenant.

Reglas:
- Un ADR de aislamiento de credenciales aplica a CUALQUIER agente que ingiera texto externo
  (WebSearch, webhooks, APIs), no solo al proceso que motivó el ADR.
- Las memorias `setup-*` documentan cómo accede LA SESIÓN principal supervisada; no son
  autorizaciones transferibles a skills/agentes persistentes.
- El agente recibe los datos tipados de quien lo invoca; la vía programática es un contrato
  de endpoints, nunca la credencial.

Lo cazó el crítico de completitud del gate de cierre, no la review de código.
