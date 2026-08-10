---
title: un dato en el bloque de contexto de un prompt LLM se lee en voz alta aunque no esté en ningún guion escrito
date: 2026-08-10
source: claude-code-session
tags: [llm, prompt-engineering, retell, voice, n8n]
---

Poner un dato "solo de referencia" (ej. `(Pol. Europolis)` junto a una dirección) en un bloque de
contexto/datos del prompt NO lo mantiene fuera de lo que el modelo dice en voz alta. Si el paciente
pregunta algo que no coincide con ninguna de las frases ya guionadas ("¿me repites la dirección
completa?", "¿en qué polígono estáis?"), el modelo improvisa leyendo el dato crudo tal cual está
escrito — incluido lo que el autor consideró "nota interna".

**Caso real**: Clínica Zen. El fix del 28-jul cambió las 3 frases guionadas de "Polígono Européolis"
a "frente al edificio de correos de la dehesa de Navalcarbón", pero dejó `(Pol. Europolis)` en el
dato de la dirección "por considerarlo no hablado". Reincidió en llamadas reales de agosto — el
modelo lo leía igual cuando la pregunta no calzaba con ninguna frase ya escrita.

**Fix real**: la instrucción de qué decir/no decir va EN LA MISMA LÍNEA que el dato, no en una
frase-ejemplo aparte: `- **Dirección** (di SIEMPRE "X"; NUNCA menciones "Y"): <dato crudo>`. Separar
la regla del dato en secciones distintas del prompt no basta — hay que anclarla al dato exacto que
el modelo va a leer cuando improvise.

Transversal a cualquier AI Agent (n8n, Retell, LangChain) con un bloque de "datos del centro/cliente"
separado del guion conversacional.
