---
title: medir un cambio contra un llm va entrelazado, y la diferencia se contrasta, no se mira a ojo
date: 2026-08-01
source: claude-code-session
tags: [evals, llm, medicion, estadistica, agh-iberica]
---
Comparar dos variantes (prompt, modelo, config) corriendo **A ×N y luego B ×N** no mide el cambio: mide la hora. El endpoint deriva. Medido en AGH con **mismo commit, payload idéntico byte a byte y `temperature: 0`**: un caso de eval pasó de **0/5 fallos a las 19:00 a 3/5 a las 00:40**, y otra rama de 83% a 20% en 4 h. Confirmado con dos arneses independientes (uno exonera al otro) y descartado el cambio de día (el prompt usaba un timestamp fijado). `MODEL_ID=gpt-4o` es el de prod → **no es del banco de pruebas: el agente rutea distinto según la hora**.

Consecuencias que no son obvias:
- Un **baseline grabado hace semanas** no es comparable con una corrida de hoy. Si el veredicto importa, el control se corre **en la misma ventana**, no se lee de un JSON.
- Repetir ×3 seguidas **no** da independencia: son tres muestras correlacionadas de la misma ventana. Más repeticiones = más confianza, no más validez.

El fix es gratis (mismas llamadas, otro orden): **una ronda dispara una llamada de CADA variante, con el orden rotado**. La deriva golpea a todos los brazos por igual y la diferencia intra-ronda sí es atribuible al cambio.

Y al leer el resultado: **nunca dos tasas a ojo**. Con n de 6-40 por brazo la aproximación normal y Newcombe declaran significativo lo que no lo es (`1/6` vs `5/6` parece abismal; Fisher exacto da p≈0.08). Usar **Fisher** para el veredicto y **Wilson** para el intervalo (la normal tiene anchura CERO en los extremos: reportaría `0/20` como «0% ± 0»). Control nulo real: **dos brazos de código idéntico dieron 33 puntos de diferencia aparente**.

Coste de aprenderlo: acusé públicamente a la PR de un compañero de una regresión inexistente; él ya había cambiado código y degradado su PR en la cola antes de que yo lo retractara. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
