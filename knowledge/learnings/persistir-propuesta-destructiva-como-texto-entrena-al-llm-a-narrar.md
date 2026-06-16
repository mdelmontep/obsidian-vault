---
title: persistir una propuesta destructiva como texto del assistant entrena al LLM a narrar en vez de llamar al tool
date: 2026-06-17
source: claude-code-session
tags: [llm, copiloto, tool-use, anthropic, openai, memoria-conversacional, anti-patron]
---
Copiloto FacturaIA, canal WhatsApp. Patrón propose/confirm: ante una acción
destructiva el runner corta y propone (botones), sin ejecutar. Para "conservar
contexto", persistía la propuesta en la memoria del hilo como **texto del
assistant** (`text = pendingConfirmation.summary`, ej. "Voy a anular la factura
X…"), sin el tool_call.

Efecto tóxico: al acumularse varias propuestas en el hilo, el modelo ve un
historial lleno de turnos assistant que responden a peticiones de acción con
prosa "Voy a [acción]…", y en el siguiente turno **imita ese patrón** → narra la
acción en texto en vez de llamar al tool → el runner no devuelve
`pendingConfirmation` → no salen botones (acción colgada). Falla probabilístico:
con 0-1 ejemplos funciona, con 3+ se rompe. Por eso las primeras acciones de un
hilo iban y la enésima no.

Fix: NO persistir la propuesta como texto. Representarla como ciclo
**tool_use → tool_result sintético** (`status:'pending_user_confirmation'`,
summary dentro del result). El historial entrena la conducta correcta (llamar al
tool) y, de paso, evita el tool_use huérfano que rompe el replay de OpenAI.
Remedio inmediato: limpiar la memoria del hilo (los ejemplos tóxicos ya escritos
siguen envenenando hasta que se purgan). Few-shot implícito del historial > las
reglas del system prompt: lo que el modelo VE hacer pesa más que lo que se le
DICE. Relacionado: [[smoke-insert-directo-no-ejerce-el-motor-real]].
