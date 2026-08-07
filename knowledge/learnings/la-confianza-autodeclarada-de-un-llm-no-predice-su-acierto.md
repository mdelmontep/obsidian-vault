---
title: La confianza autodeclarada de un LLM no predice su acierto
date: 2026-08-07
source: TuFacturaIA · Obras · sugerencias IA del tipo de mano de obra (IET)
tags: [learning, ia, evaluacion, facturaia, obras]
---

Un pipeline de sugerencias con LLM guardaba `confianza` junto a cada propuesta.
La tentación era obvia: aceptar en lote todo lo que superase 0,8 y ahorrarse la
revisión de 1.433 materiales.

**Medido contra ground truth**, usando los 43 materiales cuyo valor real conocíamos
por otra vía (el volcado del ERP legado):

| | |
|---|---|
| Dentro del ±10 % del real | 19/43 (44 %) |
| Dentro del ±25 % | 23/43 (53 %) |
| Se pasa de más del doble | 3/43 (7 %) |
| Error medio / mediano | 131 % / 23 % |
| Confianza autodeclarada media | 0,822 |

Casos concretos con confianza **0,90**: un valor real de 0,186 sugerido como
0,05 (−73 %) y otro de 0,06 sugerido como 0,009 (−85 %). Con **0,80**: un 0,014
sugerido como 0,54, un **+3.757 %**.

La confianza no separa los aciertos de los fallos: los errores grandes tienen la
misma confianza alta que los aciertos. Como umbral de auto-aceptación **no filtra
nada**, solo da la sensación de haber filtrado.

**Qué hacer en su lugar**: buscar un ground truth aunque sea parcial (aquí,
43 casos de 1.433) y medir el acierto real antes de decidir el umbral. Si no hay
ground truth posible, no hay auto-aceptación posible: revisión humana o nada.
Y donde el dato bueno ya existe por otra vía, la IA no debe pisarlo — se usa solo
donde no hay dato.

Relacionado: [[dos-piezas-en-la-misma-unidad-equivocada-dan-el-resultado-correcto]] ·
[[gate-agentico-que-no-dispara-suele-estar-inanido-no-mal-calibrado]]
