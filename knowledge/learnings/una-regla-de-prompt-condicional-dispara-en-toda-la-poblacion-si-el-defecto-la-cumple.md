---
title: una regla condicional de prompt dispara en toda la población si el valor por defecto la cumple
date: 2026-08-15
source: claude-code-session
tags: [prompting, llm, elphis, anti-patron]
---

**Caso real (Centro Elphis, 2026-08-15):** al exponerle al bot la cita sincronizada desde Doctoralia, escribí en el prompt: *"Si pone NINGUNA: no afirmes que no tiene cita… y llama a `pause_bot`"*. Correcto para quien pregunta por su cita. Pero **casi todo el que escribe al centro es un lead nuevo, y para todos ellos el contexto dice `Cita registrada: NINGUNA`** — la regla se habría disparado en la conversación por defecto y el bot habría derivado a un humano en vez de captar. Lo pillé releyendo el prompt entero al final, no al escribir la regla.

**El patrón:** una regla se redacta mirando el caso que la motivó (el 2% que pregunta por su cita) y se olvida cuál es el valor **por defecto** de ese dato en el 98% restante. Si el valor por defecto satisface la condición, la excepción se convierte en la norma.

**Regla:** al añadir una regla condicionada a un dato de contexto, pregúntate cuánto vale ese dato en la población general. Si el valor por defecto la activa, la sección necesita un guardia de ámbito explícito arriba del todo: *"ESTA SECCIÓN SOLO APLICA SI el usuario pregunta por X. En una conversación normal, ignórala."*

Vale para cualquier bloque de prompt condicionado a estado inyectado (saldo, plan, tickets abiertos, pedidos): el estado vacío es el más frecuente.

Relacionado: [[un-prompt-es-una-superficie-con-localidad-no-un-documento]] · [[llm-prompt-bloque-contexto-presupone-rol-fijo-bloquea-rol-nuevo]] · [[una-regla-de-prompt-que-el-modelo-cumple-a-medias-suele-ser-decidible-en-codigo]]
