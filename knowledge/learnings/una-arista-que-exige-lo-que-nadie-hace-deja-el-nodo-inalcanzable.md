---
title: una arista que exige un comportamiento que nadie tiene deja el nodo inalcanzable
date: 2026-09-08
source: centro-elphis
tags: [retell, conversation-flow, agentes-voz]
---
Un nodo de un conversation flow que no se visita nunca (0/34) parece un fallo de encaminamiento. Aquí
el encaminamiento era correcto 11/11: la condición de la arista pedía que el usuario acusara recibo
«sin preguntar nada nuevo y sin despedirse», y eso no lo hace nadie — 6 preguntaban, 5 se despedían,
cero acuses secos. El nodo era inalcanzable en la práctica.

- Antes de tocar el nodo, clasificar a mano lo que el usuario hace de verdad en ese punto. Si ninguna
  muestra encaja en la condición, el bug es la condición.
- Fix: convertir ese nodo en la salida por defecto (0/34 → 22/35) en vez de afinar la condición.
- Hermano del mismo problema: un nodo `conversation` cuyas únicas salidas dependen de que el usuario
  se despida o calle **no lo puede terminar el agente**. En tests con usuario simulado da bucle
  infinito; en llamadas reales se sostiene solo porque la gente cuelga.
- No ramificar por una variable que no existe: si no está en `response_variables` de ninguna tool, la
  rama se va siempre por el `else` en silencio. Ver [[retell-el-nodo-end-no-habla-la-despedida-necesita-nodo-propio]].
