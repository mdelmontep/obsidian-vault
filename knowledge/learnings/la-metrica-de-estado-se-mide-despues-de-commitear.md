---
title: una métrica derivada del árbol se mide después de commitear, nunca antes
date: 2026-08-15
source: claude-code-session
tags: [metodo, harness, tucrmia]
---
Si el estado del proyecto lo calcula un comando que lee el árbol y el historial (issues abiertos,
territorio pendiente de auditar, verificaciones caducadas), **el número que se escribe en el registro
tiene que medirse DESPUÉS del commit**, no antes de escribirlo.

Caso: cerré una iteración anotando «quedan 111 unidades» y el comando imprimía **113** sobre ese mismo
árbol limpio. El commit que estaba cerrando subió dos señales por sí solo — amplió el territorio de una
lente de auditoría y dejó una verificación sin registrar. No fue un typo: fue medir antes de que el
trabajo existiera.

Duele más de lo que parece cuando ese número **es la condición de parada** del bucle que gobierna la
sesión: el registro pasa a mentir justo sobre cuándo hay que parar. Lo encontró una lente adversarial
que cruza «lo que la documentación AFIRMA» contra «lo que los comandos HACEN», no yo releyendo.

Corolario probado en el acto: al corregirlo, la cifra volvió a cambiar (146 antes del commit, 147
después). La regla se aplicó a sí misma en la misma iteración.
