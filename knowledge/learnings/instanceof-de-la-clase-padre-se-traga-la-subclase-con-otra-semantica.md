---
title: instanceof de la clase padre se traga la subclase que significa otra cosa
date: 2026-09-14
source: agh-iberica
tags: [errores, typescript, diseno, regresion]
---
`ZipTooLargeError extends UnreadableZipError` era cómodo para los consumidores que solo querían «no se puede leer». Pero un consumidor nuevo usó `err instanceof UnreadableZipError` para decidir **«documento corrupto → 400, no se guarda»**, y se llevó dentro el tope de ratio de descompresión.

Resultado: **DOCX válidos rechazados** (3.000 párrafos vacíos con ratio 223, tabla de 8.000 filas con ratio 202, ZIP64 de Info-ZIP), con los tests en verde porque solo había fixture del caso corrupto.

Patrón:
- Cuando una subclase significa **límite de recursos** y el padre **dato inválido**, el `instanceof` del padre es la pregunta equivocada. Excluir la subclase de forma explícita (`&& !(err instanceof ZipTooLargeError)`), o no heredar.
- Cada rama nueva que decide por jerarquía necesita el **contrafáctico**: un fixture de la subclase que debe ir por el otro camino. Sin él, la aserción de rechazo es verde por construcción.

Caso: agh-iberica #1697, R9/4b (`src/hr/documents/extract-worker.ts`). Ver [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]].
