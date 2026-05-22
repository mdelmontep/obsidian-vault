---
title: LLM safety-critical — un solo tool, no cascada de tools en orden estricto
date: 2026-05-22
source: claude-code-session
tags: [llm, tool-calling, safety, design]
---

Cuando una acción del LLM es safety-critical (crisis suicida, emergencia médica, alerta de fraude), NO orquestes "primero llama X para loggear, luego Y para actuar". Bajo presión emocional/contextual el LLM puede invertir el orden, saltarse uno, o tardar más entre llamadas. La acción crítica se ejecuta tarde o nunca.

Patrón seguro:
- **1 solo tool** que ejecuta la acción crítica (transferencia SIP, bloqueo de transacción, etc.).
- **Side-effects** (logs, alertas internas al equipo, métricas) van fuera de la conversación: webhook post-evento, trigger de DB, cola asíncrona.

El LLM solo tiene que recordar "una cosa" en el momento de riesgo. La auditoría/alerta llega segundos después, suficiente para que el equipo humano reaccione sin haber bloqueado la acción crítica.

Aplica a cualquier LLM con tool-calling en dominios de riesgo: médico, financiero, legal, seguridad pública.

Caso real Elphis 2026-05-22: agente Laura tenía `transferir_crisis` (log+alerta) + `transfer_to_emergency` (SIP real) en cascada. Riesgo de que olvidara el primero o el segundo. Solución: solo el built-in, alerta movida al `call_analyzed` post-webhook.
