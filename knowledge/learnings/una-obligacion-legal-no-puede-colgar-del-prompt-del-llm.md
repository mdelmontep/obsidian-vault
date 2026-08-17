---
title: una obligación legal no puede colgar del prompt del LLM — el art. 50 se cumple en el flujo
date: 2026-08-17
source: claude-code-session
tags: [agentes, llm, legal, ai-act, determinismo, elphis, retell, chatwoot]
---
Desde el **2-ago-2026** aplica el art. 50.1 del Reglamento (UE) 2024/1689: un sistema que interactúa
con personas tiene que informar de que es una IA **a más tardar en la primera interacción**, y el 50.5
exige que sea "clara y distinguible". Multa hasta 15 M€ o 3 % (art. 99.4.g). Afecta a **todos** los
bots de voz y chat de la agencia, no solo al que te lo pidan.

- **Va en el flujo, no en el prompt.** Si el aviso depende del modelo, el día que no lo diga el
  incumplimiento es **silencioso**: nadie mira las conversaciones en las que el bot se saltó una línea.
  En Elphis es un Code node que prefija el texto al `reply_text` antes de postear. Mismo criterio que
  [[una-regla-de-prompt-que-el-modelo-cumple-a-medias-suele-ser-decidible-en-codigo]].
- **La marca de "ya avisado" no puede leerse del historial**: la API de Chatwoot devuelve solo los
  últimos 20 mensajes, así que un historial corto miente. Va en los `custom_attributes` de la
  conversación. Si el PATCH de la marca falla, se repite el aviso — informar de más es el fallo
  aceptable, no informar no lo es.
- **"Asistente virtual" a secas no basta**: en España nombra desde hace años menús de voz y bots de
  FAQ, y no despeja lo que la norma quiere despejar. Nombra la IA.
- **En voz, escribe "inteligencia artificial", no la sigla**: el TTS lee inestable las siglas de dos
  letras y el oyente no ve el texto. En chat, "IA" vale.
- El prompt sigue haciendo falta para lo que no es determinista: nunca afirmar ser humano y decirlo
  claro si preguntan.
