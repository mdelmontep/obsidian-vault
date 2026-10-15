---
title: un payload guardado para reejecutar debe volver a pasar el schema de entrada
date: 2026-10-16
source: agency-portal (Pizarra, PR #821)
tags: [zod, validacion, propuestas, testing]
---
- Patrón: se valida una op con Zod, se guarda la SALIDA (jsonb) como propuesta y al confirmar se vuelve a parsear con el schema de ENTRADA.
- Gotcha: la salida no es una entrada válida. Campos normalizados a `null` (teléfono, web, textos) chocan con `.optional()` (solo admite `undefined`), y transformaciones (etapa texto→objeto) no son idempotentes. Resultado en prod: «La operación guardada no es válida: descártala» en todas las propuestas de lead.
- Los tests no lo ven porque prueban parse y ejecución por separado, nunca parse→guardar→parse.
- Fix: `.nullish()` en los campos que la salida deja a null; deshacer la transformación antes de re-parsear (`withStageAsText`); y un **test de ida y vuelta** con un payload real: `parse(input)` → `JSON.parse(JSON.stringify(...))` → `parse` de nuevo, y que no lance.
- Ojo con arreglarlo con `z.union` de entrada|salida: tapa los mensajes de error buenos de cada rama con «Invalid input».
