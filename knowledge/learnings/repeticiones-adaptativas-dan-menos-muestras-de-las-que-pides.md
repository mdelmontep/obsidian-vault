---
title: un arnés con repeticiones adaptativas te da menos muestras de las que pides, y el log dice ×5
date: 2026-08-07
source: claude-code-session
tags: [evals, medicion, estadistica, testing]
---
Una herramienta de medición que **repite solo lo inestable** (para ahorrar llamadas de pago) deja los
casos estables con **una sola muestra**. El log sigue imprimiendo «corrida 3/5», así que el número de
repeticiones que pediste **no es el n que obtuviste** — y si de ahí derivas un umbral, el umbral es
basura con pinta de rigor.

Caso real (AGH #1002): derivar suelos por fichero de eval. Con el histórico local presente, las
pasadas 2..N eran adaptativas: `delete-routing` habría dado **n=8 en vez de 40** → Wilson inferior
**0.63 en lugar de 0.91**. Se apartó el histórico antes de **cada** invocación (la segunda ya vería el
que escribió la primera).

- Antes de medir, comprueba **qué hace la herramienta con su caché/histórico**, no lo que promete el
  flag. Y confirma el n **en la salida** (`35/35 muestras`), no en el flag que pasaste.
- El suelo se pone al **Wilson inferior de lo observado**, redondeado a la baja — nunca 0.9 por
  defecto: con 3 casos, un 0.9 está por encima de lo que la muestra sostiene y produce rojos crónicos
  que se atribuyen a la rama que toque correr. Hermano de [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]] y de [[e2e-baseline-contra-main-antes-de-culpar-a-tu-rama]].
- Corolario barato: derivar N umbrales **no** exige la corrida completa. Mide los casos que tocas.

Hermana: [[repeticiones-desiguales-por-caso-sesgan-la-tasa-pooled-compara-con-media-por-caso]] —
misma causa (repeticiones adaptativas), la otra consecuencia: cómo COMPARAR tasas con muestreo
desigual sin leer un delta que no existe.
