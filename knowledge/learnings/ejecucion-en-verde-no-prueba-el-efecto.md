---
title: una ejecución en verde no prueba que el efecto ocurriera
date: 2026-08-03
source: claude-code-session
tags: [observabilidad, n8n, agentes, verificacion]
---
`success` significa "no explotó", no "hizo su trabajo". Un workflow puede terminar en verde
cientos de veces sin alcanzar el nodo que manda el WhatsApp, crea la cita o registra el lead.

Casos reales el mismo día: Clínica Zen, **268 ejecuciones seguidas en `success` y cero envíos**
(ninguna pasó del nodo de filtrado); antes, los recordatorios llevaban MESES sin salir con todas
las ejecuciones en verde. Y el chatbot de Agentesia perdía un lead por ejecución, también en verde
([[error-de-tool-de-ai-agent-no-marca-la-ejecucion-como-fallida]]).

**Qué medir en su lugar:** que el nodo de efecto aparezca en el `runData` de la ejecución
(`/executions/{id}?includeData=true`), o el contador en el sistema de destino (cita en Calendar,
lead en el CRM). Y separar los workflows de **cron** (si no corren, están rotos) de los de
**webhook** (si no corren, es que nadie escribió) — sin esa distinción el informe se llena de
rojos falsos y se aprende a ignorarlo.

Implementado en `~/.claude/scripts/agentes-check.py`. Ver [[agentes-cliente-tres-capas]].
