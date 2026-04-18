---
title: clinica zen transfer_call no configurado en retell
date: 2026-04-18
source: claude-code-session
tags: [clinica-zen, retell, bug]
---

El prompt del agente de voz de Clínica Zen (agent `agent_7f07f61069347284a86a10ea24`) referencia `transfer_call` en múltiples secciones (objeciones, escalado a humano, tabla de herramientas), pero la tool no está definida en `general_tools`.

Resultado: Sara dice "te paso con una compañera" pero la transferencia no ocurre. La llamada se queda colgada.

Pendiente: añadir `transfer_call` como tool en la config del agente Retell, o usar el tipo built-in de Retell si lo soporta.
