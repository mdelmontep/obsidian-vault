---
title: un gate "n≥50 y acierto ≥95%" no sostiene el 95% — usa cota inferior de Wilson
date: 2026-07-25
source: claude-code-session
tags: [harness, loops, estadistica, agentes, gates]
---

Al diseñar el gate que abre la auto-aplicación de un agente ("≥50 decisiones en 30d **AND** acierto ≥95%"), el umbral es un **estimador puntual** y con n pequeño no significa lo que parece.

Wilson 95% para p̂=0,95 con n=50 → **[0,851 , 0,984]**: un intervalo compatible con el criterio de *cierre*. En números concretos, a n=50 "≥95%" es "≤2 errores":
- una org cuyo acierto real es **90%** tiene **11,2%** de probabilidad de abrir el gate;
- una cuyo acierto real es **95%** tiene **7,5%** de ser degradada por ≥3 errores en 20.

Y si el sweep corre **a diario** sobre ventana móvil, es un test de hipótesis repetido sin corrección: a lo largo de meses ambos falsos veredictos pasan de "posibles" a casi seguros. La histéresis (abrir 95 / cerrar 90) protege del ruido de la **señal**, no del ruido de **muestreo** — es el error de diseño que se cuela.

Correcciones baratas:
- Decidir por **cota inferior de Wilson**, no por p̂. Y afirmar lo que la cota sostiene: "≥90% con 95% de confianza", no "≥95%".
- Frecuencia acorde a la ventana: sweep **semanal**, condición sostenida 2 sweeps, **cooldown** (p.ej. 14d) entre cambios de estado. Mata casi todo el flapping.
- **Cobertura** como condición aparte: `resueltas / decisiones_totales`. El silencio del humano no es aceptación; con cobertura baja el gate no abre.
- Descontar el sello de goma: confirmaciones en bloque y clics a <3 s no entran en el denominador (excluirlas, no contarlas como fallo).
- Umbral propio por dominio: uno que muta estado fiscal no puede compartir el de uno cosmético; añade veto duro por un solo fallo con efecto visible al cliente.

Relacionado: [[aceptar-sugerencia-hitl-debe-cerrar-decision-o-el-gate-no-abre]] · [[gate-agentico-que-no-dispara-suele-estar-inanido-no-mal-calibrado]] · [[watchdog-umbral-debe-tolerar-un-tick-perdido]].
