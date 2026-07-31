---
title: para derivar copy de la capacidad real, usa el flag que gobierna comportamiento, no el descriptivo
date: 2026-07-31
source: claude-code-session
tags: [copy, type-safety, metadatos, tests]
---
Al hacer que un texto de UI se calcule desde metadatos en vez de mantenerse a mano
(«¿este panel hace cambios?»), la tentación es contar el flag que *describe* la
propiedad. En un registro de 94 tools, contar `readonly !== true` daba **53 que
escriben** — falso: `readonly` documenta «certificado sin efectos secundarios» para
memoizar, su default es `false` conservador, y la mayoría de tools de solo lectura no
lo llevan.

El flag correcto era `destructive`, que está bien mantenido **porque gobierna
comportamiento real**: sin él el servidor no exige `confirmed_by_user_id` y no
devuelve 412. Un flag con consecuencias se mantiene solo; uno documental se pudre.

Regla: antes de derivar nada de un metadato, pregunta qué se rompe si está mal. Si la
respuesta es «nada», el número que saques no vale.

Y al escribir el test que ata texto y capacidad: comprueba la **llamada**, no la
palabra. Un `expect(fuente).not.toContain('orgHasFeature')` falla contra los propios
comentarios que explican por qué ya no se usa; `not.toMatch(/\bawait\s+orgHasFeature\s*\(/)` no.

Caso real: FacturaIA `qa-024` (#1408) y `qa-020` (#1410).
