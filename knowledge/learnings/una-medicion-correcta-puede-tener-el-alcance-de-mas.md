---
title: una medición correcta puede tener el alcance de más
date: 2026-08-10
source: claude-code-session
tags: [metodo, verificacion, whatsapp, agh-iberica]
---
Medido contra la API de Meta: un **parámetro** de plantilla con `\n` devuelve `[132018] Param text cannot have new-line/tab characters…` y no entrega. Cierto y comprobado.

De ahí se escribió en el código *«el digest no puede ser una lista con saltos de línea»*, y se diseñó el arreglo alrededor de esa frase. **Falso**: la restricción es del parámetro, no del mensaje — el **cuerpo** de la plantilla sí admite saltos. Se comprobó dando de alta una multilínea, que Meta aprobó y entregó con los saltos intactos.

El error no estuvo en medir ni en el resultado: estuvo en **el alcance del enunciado**. Se midió el objeto A y se concluyó sobre el conjunto que lo contiene. Y como la conclusión venía etiquetada de «medido contra la API, no heredado de un comentario», quedó blindada contra la duda propia y ajena.

**Patrón:**
- Al escribir la conclusión, nombrar **el objeto exacto medido**: «el parámetro», no «el mensaje»; «esta ruta», no «el sistema». Si la frase abarca más que lo medido, es hipótesis y se marca como tal.
- Sospechar de todo **«X es imposible»** sacado de probar **una sola forma** de hacer X. Preguntarse *¿por dónde más podría entrar esto?* — aquí la respuesta estaba a un POST de distancia.
- Antes de gastar un experimento, buscar un **experimento natural**: ¿hay algo ya en producción que conteste? (Aquí no lo había, pero costó una lectura comprobarlo.)

Ver [[una-afirmacion-repetida-no-es-una-verificacion]], [[resolver-el-destinatario-por-su-clave-no-por-recencia-ni-sufijo]].

**Tercera vez el mismo día, y la firma es siempre igual: leer UNA función y afirmar el comportamiento de
la CADENA** (FacturaIA 11-ago). Vi que `tieneActividad` era `aprobadas > 0 || pendientes > 0`, concluí
que el digest enviaría el correo con `aprobadas: 0`, y publiqué que «el 100 % de los correos que envía
hoy llevan el titular *aprobó 0 facturas*» — en un commit, en el cuerpo de un PR y en el registro de QA.
Falso: el llamante tenía un guard más, `if (summary.aprobadas === 0 || !tieneActividad(...)) continue`,
así que ese caso **no era alcanzable**. Lo desmontó el primer run real: `enviados: 0, sinActividad: 4`.

Lo que hay que hacer y no hice: **leer la costura donde se DECIDE, no la función que calcula el dato**.
Una función auxiliar te dice qué computa; solo el llamante te dice qué se hace con eso. Y el atajo que
lo habría evitado costaba menos que la corrección: **ejecutarlo una vez antes de afirmar**. Las tres
veces del día tuvieron la misma cura (ejecutar / preguntar la pregunta exacta / mirar el universo) y el
mismo síntoma: una conclusión creíble, publicada, y con la etiqueta de «medido» encima.
