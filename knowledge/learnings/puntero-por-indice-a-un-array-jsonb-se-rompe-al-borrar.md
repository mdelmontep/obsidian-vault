---
title: apuntar por índice a un array JSONB se rompe en silencio al borrar un elemento
date: 2026-08-29
source: facturaia
tags: [jsonb, postgres, identidad, ocr, diseño]
---

Al guardar en una tabla puente una referencia a «la línea N del array `datos_extraidos.lineas`», el
puntero es la posición. La UI que edita ese array borra con `lineas.filter((_, i) => i !== idx)`:
todos los índices por debajo se desplazan y el puntero pasa a señalar **otra línea**, sin error.

Peor con el remedio intuitivo: fichar el contenido (producto + cantidad + importe) para detectar la
deriva. Con dos líneas idénticas —lo normal en un albarán— la huella sigue casando después del
desplazamiento, así que el candado no ve nada.

El arreglo no es un candado mejor: es dar **identidad estable** a cada elemento. Un `uuid` por línea,
acuñado perezosamente en el primer sitio que la toca (cliente y servidor, los dos), y la tabla puente
apunta a ese id. Entonces borrar una línea deja el cruce huérfano de forma **visible**, que es lo que
querías.

Y si el candado depende de la identidad, no lo cierres contra el contenido: comprueba cuál de las dos
cosas estás midiendo de verdad.
