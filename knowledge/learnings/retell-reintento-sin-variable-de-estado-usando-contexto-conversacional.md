---
title: retell conversation flow puede distinguir "primer fallo" de "ya reintentado" sin variable de estado
date: 2026-08-12
source: claude-code-session
tags: [retell, conversation-flow, patron]
---
Un nodo `function` que falla no tiene por qué escalar a preguntar al cliente "¿lo intento otra
vez?" (mala UX: pregunta que rompe el flujo natural). Patrón de 2 niveles sin backend ni variable
de estado explícita:

1. Edge de éxito: `transition_condition` deja de ser "Always after function call" y pasa a "resultado
   normal (éxito, o un resultado válido como 'no encontrado') — NO fallo/vacío/atascado".
2. Edge nuevo "primer fallo": condición "no devolvió resultado usable, Y es la PRIMERA vez que pasa
   para esta acción en esta llamada" → nodo que dice una frase breve y natural ("no me ha cargado
   bien, un segundo que lo miro otra vez") y transita SIEMPRE de vuelta al mismo nodo function —
   sin preguntar nada.
3. Edge nuevo "fallo tras reintento": condición "ha vuelto a fallar DESPUÉS de que ya se hubiera
   reintentado una vez para esta misma acción" → nodo con frase de cierre definitiva + escalar.

El LLM evalúa las `transition_condition` tipo prompt con el historial completo de la conversación —
puede inferir "ya pasé por el nodo de reintento antes" sin que exista ninguna variable/contador
explícito en el sistema. No hay riesgo de bucle infinito porque el 3er intento nunca vuelve al nodo
de reintento, va a escalar.

Verificar integridad de los 3 edges por nodo function antes de publicar: ningún par de condiciones
debe poder evaluarse ambas a la vez (ambigüedad → comportamiento no determinista).
