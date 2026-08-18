---
title: una obligación legal no puede colgar del prompt del LLM — el art. 50 se cumple en el flujo
date: 2026-08-17
source: elphis
tags: [agentes, llm, legal, ai-act, determinismo, elphis, retell, chatwoot]
---
Desde el **2-ago-2026** aplica el art. 50.1 del Reglamento (UE) 2024/1689: un sistema que interactúa con
personas informa de que es una IA **a más tardar en la primera interacción**, y el 50.5 exige que sea
"clara y distinguible". Multa hasta 15 M€ o 3 % (art. 99.4.g). Afecta a **todos** los bots de la agencia.

- **Va en el flujo, no en el prompt**: si depende del modelo, el día que no lo diga el incumplimiento es
  silencioso. En Elphis, un Code node prefija el texto al `reply_text`. Ver
  [[una-regla-de-prompt-que-el-modelo-cumple-a-medias-suele-ser-decidible-en-codigo]].
- **La marca de "ya avisado" no puede leerse del historial**: Chatwoot devuelve solo los últimos 20
  mensajes. Va en `custom_attributes` — y el PATCH tiene que **fusionar**, no reconstruir: reconstruirlo
  borraba la marca en cada turno y el bot se presentó 17 veces en una conversación (18-ago).
- **Un fragmento que inyecta el sistema se trae el recorte de lo que duplica.** El aviso abre con "Hola,
  soy Laura…" y el modelo abría con su propio saludo: dos saludos. No es arreglable en el prompt (en el
  2.º mensaje no se antepone nada y ahí sí debe saludar), así que el nodo que añade el aviso recorta el
  saludo de apertura. Y escribir la frase literal en el prompt hizo que el modelo la copiara: salía dos
  veces. **Si lo pone el sistema, el prompt no lo menciona; si el prompt puede solaparlo, el sistema lo
  recorta.** Corolario: lo que deba salir SIEMPRE va en texto fijo — pedido al prompt salió 0/5.
- **"Asistente virtual" a secas no basta** (nombra menús de voz desde hace años): nombra la IA. En voz
  escribe "inteligencia artificial", que el TTS lee inestable las siglas de dos letras; en chat "IA" vale.
- El prompt sigue haciendo falta para lo no determinista: nunca afirmar ser humano, y decirlo si preguntan.
