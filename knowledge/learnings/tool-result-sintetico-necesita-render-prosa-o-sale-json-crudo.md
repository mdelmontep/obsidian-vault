---
title: tool_result sintético persistido para el LLM necesita render en prosa o sale JSON crudo al usuario
date: 2026-06-25
source: claude-code-session
tags: [llm, copiloto, tool-use, ui, anti-patron]
---
Para no entrenar al modelo a narrar ([[persistir-propuesta-destructiva-como-texto-entrena-al-llm-a-narrar]]), una propuesta destructiva del Copiloto se persiste como tool_use→tool_result **sintético** `{status:'pending_user_confirmation', summary}`. Consecuencia no prevista: al recargar el hilo, la card de UI cae al `case default` (no hay renderer para ese "tool") y pinta el objeto crudo (`JSON.stringify` en un `<pre>`) → el usuario ve JSON.

Patrón: cualquier payload estructurado que persistas para el modelo puede acabar en la UI. **Doble defensa:**
- **Presentación (dura)**: la card NUNCA hace `JSON.stringify` del result; deriva prosa (prioriza `summary`/`message`; si no, frase de `count`/`found`). Sin `<pre>`/`<code>` hacia el usuario.
- **Contrato**: system prompt "responde siempre en prosa" + sanitizador en el runner que descarta el `text` del assistant si es un objeto/array JSON serializado.

Relacionado: [[llm-tool-use-card-visual-instruir-no-duplicar-lista]].
