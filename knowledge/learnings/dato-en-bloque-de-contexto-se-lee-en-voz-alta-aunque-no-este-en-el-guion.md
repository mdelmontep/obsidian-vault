---
title: la regla que prohíbe usar un dato va pegada al dato, no en su propia sección del prompt
date: 2026-08-10
source: clinica-zen, elphis
tags: [llm, prompt-engineering, retell, voice, chat, n8n, clinica-zen, elphis]
---
Un dato "solo de referencia" en el bloque de datos del prompt NO se queda fuera de lo que el modelo dice.
Cuando la pregunta no calza con ninguna frase guionada, el modelo improvisa leyendo el dato crudo tal cual
—incluido lo que el autor consideró nota interna—, y la regla que lo prohíbe, si vive en otra sección, no
se activa porque el modelo no está en ese flujo.

**Clínica Zen (jul-ago)**: el fix cambió las 3 frases guionadas de "Polígono Européolis" a otra referencia,
pero dejó `(Pol. Europolis)` en el dato de la dirección "por no hablado". Reincidió en llamadas reales.

**Elphis (18-ago), mismo patrón en chat**: el horario del centro estaba en la ficha de arriba y la
prohibición ("no des horas de la primera visita, que las vea en el enlace") 157 líneas más abajo, dentro de
«Flujo de reserva». A un "¿horario de visitas?" el modelo no estaba reservando, así que sirvió el horario
del centro como el de la visita. Medido, 5 tiradas del turno real: **2/5 daba horas; con el aviso pegado al
dato, 0/5** y 5/5 remite al enlace.

**Fix**: la instrucción va EN LA MISMA LÍNEA que el dato —`- **X** (di SIEMPRE "A"; NUNCA "B"): <dato>`—,
además de en su sección. Que la regla exista no basta: tiene que estar donde el modelo mira al improvisar,
y eso es el dato. Corolario: lo que deba salir siempre, en texto fijo, no en el prompt (medido 0/5). Ver
[[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]].
