---
title: comparar tasas agregadas con muestreo DESIGUAL por ítem (pooled) sesga hacia lo que más se repite — compara con media por ítem
date: 2026-08-04
source: claude-code-session
tags: [evals, estadistica, llm, agh]
---
Caso AGH (#858): al pasar de "todos los casos ×3 fijo" a repeticiones ADAPTATIVAS (estables ×1,
inestables ×3-5), comparé a ojo el `passed/total` por eje entre una corrida antigua (muestreo
uniforme) y la nueva (muestreo desigual): deltas de hasta 14 puntos que parecían un problema real
en un eje (composition, query). Con la función real del proyecto (`caseRate`: media de la tasa DE
CADA caso, cada uno pesa `1/N` dé las muestras que dé), los mismos dos runs daban 0.0 de delta en
esos ejes — el "problema" era el propio sesgo de lectura, no el código.

Por qué diverge: pooled (`Σpasadas / Σmuestras`) pesa cada MUESTRA por igual, así que un caso que se
repitió 5 veces pesa 5× lo que uno que se repitió 1 — y precisamente los que más se repiten son los
que fallaron o oscilaron antes. La tasa pooled queda sesgada hacia el peor comportamiento pasado,
sin que el modelo haya cambiado nada.

Regla: en cuanto el nº de muestras por ítem deja de ser constante (repeticiones adaptativas,
muestreo dirigido a casos "sospechosos", weighted sampling), NUNCA compares/agregues con
`pasadas/muestras` crudo — usa la media de la tasa POR ÍTEM. Y verifica con la función/fórmula REAL
del sistema que mides, no con una cuenta mental rápida: la lectura ingenua aquí habría bloqueado un
PR bueno por un "problema" que no existía.
