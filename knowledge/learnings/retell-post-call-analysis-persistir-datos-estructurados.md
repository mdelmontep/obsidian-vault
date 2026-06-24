---
title: retell post-call analysis para persistir datos estructurados de la llamada con latencia cero
date: 2026-06-24
source: claude-code-session
tags: [retell, voice, post-call, kommo]
---
Para capturar datos que el cliente menciona en una llamada SIN añadir latencia a la conversación: definir campos en `post_call_analysis_data` del agente (tipos enum/number/string/boolean, con descripción clara + ejemplos) → el LLM los rellena tras colgar → el handler del webhook `call_analyzed` los lee de `call.call_analysis.custom_analysis_data` y los persiste (Kommo CFs / BD).

Ventaja: cero latencia (ocurre post-llamada, no durante). Añadir un flag `*_capturado` (boolean) para escribir solo si hubo dato real. Para select/multiselect de Kommo, mapear el string a `enum_id` en el handler.

Caso real Simarro outbound: perfil de búsqueda (zona, precio, hab, m², baños, extras, estado) capturado en la llamada → CFs Kommo → `lead_preferences` → matching, sin pedir nada extra al cliente. Relacionado: [[retell-call-summary-vs-tool-args-intencion-para-resumen-email]].
