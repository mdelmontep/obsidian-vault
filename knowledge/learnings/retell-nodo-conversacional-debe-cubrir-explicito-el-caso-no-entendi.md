---
title: retell — un nodo conversacional debe cubrir explícito el caso "no entendí", o el LLM se queda a medias
date: 2026-08-12
source: claude-code-session
tags: [retell, conversation-flow, patron]
---
Un nodo con instrucción tipo "si el cliente dio X → di 'Claro.' y transita" puede fallar de forma
sutil: si la transcripción es confusa (STT imperfecto, tartamudeos) y el LLM no tiene certeza de que
se cumple la condición del edge, dice el acknowledgment ("Claro.") pero NO transita — porque
evaluó el edge como no cumplido — y tampoco cae en la rama alternativa del prompt (esa pedía "si NO
dio NINGÚN criterio", y aquí sí dio algo, solo que ininteligible). El resultado: un turno que no
transita, no pregunta, no hace nada más — el cliente se queda esperando, a veces disparando el
"¿sigues ahí?" del reminder de silencio.

Confirmado en llamada real dos veces (Simarro): relajar la condición del edge ("aunque la frase sea
confusa, cuenta como que sí dio zona") NO bastó — hacía falta una TERCERA vía explícita en el prompt
para "no reconozco nada identificable, aunque el cliente dijo algo": ahí SÍ hay que preguntar
("¿qué zona buscas?") en vez de decir la palabra suelta.

Regla general: en cualquier nodo con 2 caminos ("cumple condición" / "no dio nada"), audita el hueco
del medio — "dio algo pero no lo suficientemente claro para decidir" — y dale una salida explícita.
Sin esa tercera vía, el LLM improvisa un acknowledgment sin acción de seguimiento.
