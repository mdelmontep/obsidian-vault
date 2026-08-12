---
title: un candado derivado no se defiende de una mutación de sí mismo
date: 2026-08-12
source: claude-code-session
tags: [testing, mutacion, arnes, candados]
---
Un guard cuya expectativa se **deriva** de la fuente (la matriz sale del descriptor, la lista sale del código) es la forma correcta de evitar que una whitelist se desincronice en silencio. Pero tiene una mutación de un carácter que lo deja **tautológico y verde para siempre**: sustituir la derivación por la propia tabla — `filtrosDeclarados()` → `Object.keys(ESPERADO)`. Medido: 6 mutaciones, 5 con víctima, **ésa sobrevive**.

**No se puede tapar con otro test.** Cualquier caso que añadas volverá a leer la fuente por su cuenta y seguirá pasando, porque la mutación rompe el **enlace** entre los dos extremos, no ninguno de los extremos. Es la misma razón por la que un arnés de mutación serio filtra a código de **producción** y no muta tests: mutar un test no es una medición, es **reescribir la vara**.

**Qué hacer cuando aparece:** no buscar el test que falta. Declararla en el código con el motivo, y decir que lo que la protege es que sea **visible en review**. Escribirlo es la única cobertura posible — y un guard con su superviviente declarada es más honesto que uno que finja 6/6.

**Corolario, mismo día:** si un lote de mutaciones sale con **todas** sin víctima, sospecha del instrumento antes que del código. Un `git commit` que falló se comió el heredoc con la variable del comando de test, y las cuatro salieron «sin víctima» — iba a apuntar cuatro huecos inexistentes. Un resultado uniformemente negativo es señal de arnés.

Vecino, otra familia: [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]].
