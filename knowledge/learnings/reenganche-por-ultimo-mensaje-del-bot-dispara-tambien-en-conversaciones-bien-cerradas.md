---
title: reenganche que dispara por "último mensaje fue del bot + pasó tiempo" reabre conversaciones ya cerradas bien
date: 2026-08-04
source: claude-code-session
tags: [n8n, kommo, whatsapp, reenganche]
---

Un workflow de "reenganche de conversaciones abandonadas" que dispara con la condición
`último_mensaje.tipo = 'ai' AND tiempo_transcurrido > X` es un falso positivo estructural: **toda**
conversación bien terminada también acaba con el bot teniendo la última palabra (la despedida) y
luego silencio. Esa condición no distingue "el paciente se fue a medio flujo" de "el paciente dijo
gracias y se despidió" — las dos formas de "el bot habló último y nadie contestó" son indistinguibles
sin mirar el CONTENIDO del último turno.

**Caso real**: Clínica Zen, paciente reservó cita, se despidió con "Gracias!", el bot respondió
"A ti. Que tengas buen día" — y 70 min después el workflow le mandó "¿Sigues por ahí?" igual.

**Fix aplicado**: en la query SQL, además de mirar que el último mensaje sea del bot, mirar el
último mensaje del HUMANO y excluir la sesión si es un cierre corto reconocible (`gracias`, `vale
gracias`, `adiós`, `nada más`... con regex anclado `^...$` para no capturar frases más largas que
contengan esas palabras de paso). No es NLU perfecta, pero corrige el caso mayoritario sin tocar
el Agente ni añadir estado nuevo.

Transversal: cualquier cliente con un workflow de reenganche/reactivación de leads (Danny,
Laserys, EcoBox, Simarro, Elphis) puede tener la misma lógica y el mismo falso positivo.
