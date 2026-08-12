---
title: math.round(x*100) !== x*100 rechaza importes de 2 decimales legítimos
date: 2026-08-12
source: claude-code-session
tags: [typescript, validacion, dinero]
---
Validar «máximo 2 decimales» con `Math.round(x*100) !== x*100` falla con
importes normales por coma flotante: `19.99*100 = 1998.9999999999998` y
`10.05*100 = 1005.0000000000001` → el 400 salta sobre valores correctos.
Los tests no lo cazan si solo prueban valores «limpios» (30.123, 10.999).

Fix: redondear ANTES de comparar — `Math.round(x*100)/100 !== x` (acepta
19.99/10.05, rechaza 10.999). Test de regresión con 19.99 y 10.05 siempre.

Caso real: TuFacturaIA #1666 (topes de contenido), cazado por el revisor de
spec; un superadmin no podía fijar el tope de vídeo en 19,99 €.
