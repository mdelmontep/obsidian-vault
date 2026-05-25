---
title: retell execution_message_description no debe comprometer la acción futura
date: 2026-05-25
source: claude-code-session
tags: [retell, voice, tools, prompt-engineering]
---

`execution_message_description` es lo que Retell le pide al LLM que diga **mientras la tool se ejecuta** (cubre el silencio del HTTP request). Si redactas algo como "Dile que estás registrando la llamada para derivarla a la persona adecuada", el LLM lo verbaliza tal cual **antes** de saber si va a derivar.

Caso Tecnocloud: con esa frase, Laura decía "Voy a registrar la llamada para derivarla a la persona adecuada para solucionar su problema" en el primer turno, ignorando que el flujo correcto era preguntar el motivo primero. La frase la empujaba a disparar la tool antes de tiempo.

Regla: el `execution_message_description` debe ser **neutro** y solo cubrir el silencio. Ejemplos válidos:
- "Dile algo natural y breve tipo 'Dame un segundo que lo registro...' "
- "Dile que estás apuntándolo, sin prometer nada."

Prohibido prometer derivación, transferencia, resolución u otra acción que aún no se ha decidido.

Específico Retell, pero patrón aplicable a cualquier provider con "speak during execution".
