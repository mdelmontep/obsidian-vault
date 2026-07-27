---
title: un arnés de smoke con asserts de eco y falso verde no detecta nada — y al arreglarlo encuentra bugs solo
date: 2026-07-27
source: claude-code-session
tags: [testing, evals, agentes-conversacionales, arnes]
---
Escenario de smoke de un agente conversacional que reportaba «9/9 OK» y **no habría detectado ninguno de los 13 fallos** de una llamada real. Dos vicios, ambos frecuentes en arneses escritos a mano:

1. **Falso verde**: un turno que lanzaba excepción hacía `continue` sin registrar checks → `passed === totalChecks` seguía cumpliéndose y el proceso salía `0`. Fix: la excepción cuenta como fallo de todos los checks declarados de ese turno, y `turnosEjecutados !== turnosDeclarados` fuerza exit ≠ 0.
2. **Asserts de eco**: `containsAny(["Dragados","nube"])` sobre un turno donde el usuario acaba de decir «Dragados» y «nube» → el modelo repite por eco y pasa sin medir nada. Fix: verificar contra **datos sembrados que el turno no pronuncia**, o contra el **payload estructurado** de la acción (que `fireAt` caiga en jueves calculado con `Intl.DateTimeFormat`, no buscar «jueves» en el texto).

Otros dos que aplican igual: comprobar **todas** las acciones del batch (no solo `actions[0]`, o un write colado en 2.ª posición es invisible) y componer **igual que producción** (con los decoradores reales: onboarding, serialización, tono) o el arnés no puede reproducir clases enteras de bug.

**Lo que lo valida:** el arnés arreglado, en su PRIMERA pasada con modelo real, destapó un bug que no venía de la llamada. Un arnés que no encuentra nada nuevo el día que se arregla, probablemente sigue midiendo eco.
