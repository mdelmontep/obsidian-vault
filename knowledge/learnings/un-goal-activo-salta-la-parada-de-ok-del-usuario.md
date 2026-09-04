---
title: un /goal activo salta cualquier parada de ok del usuario en el prompt
date: 2026-09-05
source: mandadm
tags: [claude-code, goal, harness, prompting, agentes]
---
`/goal <condición>` (Claude Code 2.1.26x) chequea la condición al final de cada turno y, si no se
cumple, empuja a seguir. Un prompt con «presenta el resumen y espera OK» deja de tener parada: el
chequeo ve la condición sin cumplir y la sesión continúa como si el OK hubiera llegado.
Dos diseños válidos, elegir uno explícitamente en el prompt:
- **Dos goals**: el primero se cumple «al presentar el resumen», el usuario lee y lanza el segundo.
- **Sin usuario**: cada decisión que pediría OK la toma un tribunal de 3 agentes con expertises
  distintas, por mayoría, y se registra en un ADR que el usuario lee al volver (así quedó `/horda`).
Escribir en la propia condición «ninguna pregunta hecha al usuario» cuando es el segundo caso.
Tope de la condición: 4000 caracteres. Solo en workspace de confianza y con hooks activos.
Caso: la horda de [[mandadm]].
