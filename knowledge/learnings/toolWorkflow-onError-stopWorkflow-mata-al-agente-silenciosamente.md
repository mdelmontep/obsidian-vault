---
title: toolWorkflow onError stopWorkflow mata al agente silenciosamente
date: 2026-04-20
source: claude-code-session
tags: [n8n, ai-agent, error-handling]
---

En nodos `toolWorkflow` conectados a un AI Agent de n8n, `onError: stopWorkflow` mata al agente entero cuando el sub-workflow falla. El usuario no recibe ninguna respuesta — el chat simplemente se congela.

**Modos disponibles**:
- `stopWorkflow` — mata todo, el usuario no recibe nada (malo)
- `continueErrorOutput` — el error llega al AI Agent como output, el agente puede informar al usuario (recomendado)
- `continueRegularOutput` — traga el error silenciosamente y devuelve output vacío (peligroso, el agente cree que todo fue bien)

**Regla**: usar SIEMPRE `continueErrorOutput` en nodos toolWorkflow del AI Agent. Así el agente recibe el error y puede decir "hubo un problema al reservar tu cita, inténtalo de nuevo" en vez de desaparecer.

Aplicado en Clínica Zen: 4 nodos tool (Reservar_cita, Cancelar_cita, Derivar_agente, Buscar_base_de_datos) cambiados de stopWorkflow a continueErrorOutput.
