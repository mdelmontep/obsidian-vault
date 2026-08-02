---
title: un test que compara dos artefactos generados de la misma constante no prueba la constante
date: 2026-08-02
source: claude-code-session
tags: [testing, mutacion, rls, generadores, tucrmia]
---
Patrón: una definición en código genera dos artefactos (p. ej. el predicado de una policy y el cuerpo de
una función SQL), y un test de propiedad recorre toda la matriz comprobando que los dos coinciden. Se lee
como una garantía fuerte. **No lo es sobre la definición**: esperado y obtenido salen de la MISMA
constante, así que cambiar una celda mueve las dos partes a la vez y el test sigue verde.

Medido en TuCRMIA con 127 mutaciones reales: de las 56 celdas de la matriz de permisos, **52 se podían
cambiar con los 168 tests en verde**. Añadir `viewer` a `member.write` pasaba limpio; poner un recurso en
eje de fila `none` daba a cualquier comercial toda la organización.

Lo que sí cubre —y muy bien— es el EMISOR: un helper mal escrito, un paréntesis de precedencia.

Fix: una tabla congelada escrita a mano desde el documento vinculante, y `expect(CONSTANTE).toEqual(TABLA)`.
Es duplicación deliberada y es lo único que convierte un cambio de permiso en un diff que alguien aprueba.
Corolario: `toContain` sobre un fichero entero es casi infalsificable si la cadena sale varias veces
(`and m.status = 'active'` salía 4 veces; borrarla de donde importaba dejaba el test verde). Acotar la
aserción al cuerpo de la función concreta. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
