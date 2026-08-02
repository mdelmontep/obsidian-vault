---
title: el OCR lee DD-MM-YY como YY-MM-DD y manda la factura a otro ejercicio
date: 2026-07-29
source: claude-code-session
tags: [ocr, fiscal, facturaia, fechas]
---

Factura con la fecha en formato corto de dos dígitos de año (`23-06-26`, `23/07/26`) → el modelo la
interpreta como `YY-MM-DD` y persiste **2023**-06-26 en vez de 2026-06-**23**. Dos documentos reales
verificados contra el papel (DAORO 10422P de Chivite y un justificante simplificado de AgentesiaLab);
en el segundo además leyó el día `23` como `29`.

No es cosmético: `fecha` manda en el 303 y en el libro de recibidas, así que la factura **desaparece
del trimestre que le toca** y aparece en un ejercicio de hace tres años. En Chivite eran 492,80 € de
base cuyo IVA soportado no se deducía donde tocaba.

Medido en prod (2026-07-29), excluyendo orgs `is_test`: **9 de 109 recibidas (8,3%)** con la fecha
desviada más de 180 días respecto a su alta. 7 seguían en `sin_aprobar` (las salva el humano al
revisar), 2 ya estaban aprobadas y sin vía de corrección en la UI.

Qué hacer:
- **Pedir el formato al modelo y desambiguar en código**, no confiar en su interpretación: con año de
  dos dígitos, `DD-MM-YY` es lo normal en factura española.
- **Sanity check barato antes de persistir**: una fecha de emisión que se aleja años del alta del
  documento es sospechosa por definición — a revisión, no a la BD.
- El nombre del fichero suele confirmar (`Facturas_0481_230626.PDF` es el mismo `DDMMYY`).

Ver [[campo-que-muestra-un-formato-y-guarda-otro-descarta-la-edicion-en-silencio]] · [[dos-campos-confundibles-pide-los-dos-y-cruzalos-en-codigo]] · [[facturaia]]

**Cerrado el 1-ago (PR #1457).** REGLA 23 + campo `fecha_literal` (la cadena impresa, sin reordenar) y `resolverFechaEmision`, que la reinterpreta como DD-MM-YY cuando el año viene en dos dígitos y **manda sobre la lectura del modelo**, con anomalía para que el cambio de ejercicio quede en la traza.

Lo que más enseña es por qué llegó a prod: **el colador ya existía**. `buildAnomalies` tenía `date_too_old`… con umbral de **10 años** y severidad **`low`**. Un salto de tres años pasaba por debajo, y un `low` no para el item. Un control calibrado para un fallo que no es el que ocurre no es un control. Ahora: 18 meses, `medium` y en `FORCE_REVIEW_TYPES`. Y se descartó añadir un segundo colador dentro del guard nuevo: serían dos sistemas opinando distinto del mismo campo.

Repaso de daño en prod tras el arreglo: quedan **5 recibidas** con la fecha >180 días desviada, todas de Laserys, todas `sin_aprobar` y subidas el mismo día — tienen pinta de carga histórica real, no de mala lectura. Las 2 de Chivite que sí lo eran están corregidas (10422P en 2026-06-23).
