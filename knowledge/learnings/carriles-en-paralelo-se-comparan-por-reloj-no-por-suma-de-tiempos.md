---
title: carriles en paralelo se comparan por reloj, no por suma de tiempos
date: 2026-09-22
source: facturaia
tags: [testing, medicion, rendimiento, playwright]
---
Al repartir una suite en carriles con distinto número de workers, sumar la duración de las
pruebas de cada carril **no** da su reloj: un carril con 3 workers parece el triple de caro
de lo que es. Comparar sumas entre carriles con paralelismo distinto es comparar unidades
distintas sin decirlo.

Medido (FacturaIA, smoke E2E de 730 pruebas, 751 s de reloj):

| carril | suma | workers | reloj |
|---|---|---|---|
| `smoke-escritura` | 668 s | 1 | **668 s ← manda** |
| `smoke-lectura` | 417 s | 3 | ~139 s |
| `smoke-api` | 414 s | 1 | 414 s |

- La conclusión sobrevivió por casualidad: los dos carriles que se comparaban iban a 1
  worker, donde suma y reloj coinciden. Contra la lectura habría dicho una tontería.
- **Antes de subir workers, mira si ese carril manda**: partir `smoke-api` en dos no bajaba
  el reloj ni un segundo, porque la tanda la fija el carril serializado.
- Y cuando el cuello está serializado **por una razón real** (38 specs compartiendo los
  datos de una org), la palanca no es config sino datos: subirle workers sin darle orgs
  propias cambia el fallo de determinista a intermitente.
- Publica siempre el número de workers al lado de la cifra, o el dato se malinterpreta solo.

Relacionado: [[el-suelo-de-un-semaforo-explica-quien-entra-no-cuanto-tarda]]
