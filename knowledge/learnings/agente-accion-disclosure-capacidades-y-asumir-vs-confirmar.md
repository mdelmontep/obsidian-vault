---
title: agente de acciones — declara capacidades, asume-lecturas / confirma-escrituras
date: 2026-07-04
source: claude-code-session
tags: [agentes, llm, prompt, conversacional, hitl]
---
"Se siente robótico / interroga en vez de ofrecer / clarify-loops" en un agente que ejecuta
acciones suele ser síntoma de un system prompt sin 3 secciones (fuentes: OpenAI Model Spec, NN/g,
Anthropic multishot):
1. **Capacidades declaradas** (catálogo cerrado): "¿qué puedes hacer?" → ofrece 3-5 opciones,
   NUNCA preguntes de vuelta (sin esto cae a clarify e interroga).
2. **Asumir-vs-preguntar por riesgo** (Model Spec): LEER = asume el caso razonable y ofrece;
   ESCRIBIR/enviar = confirma. Nunca encadenes preguntas abiertas.
3. **Few-shot (3-5)** para fijar tono natural.

Confirmaciones HITL: **resumen determinista (verbatim, generado por código) + envoltura natural**;
la persona no absorbe la lógica de tarea (OpenAI: "personalities do not override task output").
Si el texto sale de plantillas deterministas, lo robótico se arregla **en las plantillas**
(agrupar ítems), no en el prompt — el LLM ni las toca. La "naturalización por LLM" es un
trade-off aparte (coste/latencia/determinismo). Relacionado: [[hitl-resumen-debe-nombrar-entidad-desambiguada]].
