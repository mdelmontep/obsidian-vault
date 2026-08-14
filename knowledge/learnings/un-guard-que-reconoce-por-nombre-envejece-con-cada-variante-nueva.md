---
title: un guard que reconoce colaboradores por su nombre envejece cada vez que nace una variante
date: 2026-08-14
source: claude-code-session
tags: [testing, guards, arquitectura, mantenimiento]
---

Los guards de repo que barren ficheros suelen identificar al colaborador por **nombre**
(`/\bresolveSystemAlert(FireAndForget)?\b/` sobre los imports). Funciona hasta que nace una
variante legítima: al añadir `resolveSystemAlertThrottled`, sus dos ficheros pasaron a
contar como emisores de alertas **sin resolvedor** y el guard los denunció.

El guard tenía razón en denunciar y estaba mal calibrado a la vez. La corrección es ampliar
el patrón **y** dejar un caso de test con el nombre nuevo, no relajar el guard: sin ese
caso, el siguiente que invente otra variante repite el trabajo desde cero.

Señal de que un detector es de esta clase: su regex enumera nombres concretos en vez de
mirar la forma. Al escribirlo, conviene decir en el comentario que envejece así.

**Y solo lo ve la suite completa.** `lint` + `typecheck` + `build` pasaron limpios con este
guard en rojo, y los tests dirigidos del área tocada tampoco lo incluyen: un guard de
arquitectura vive en su propio fichero, lejos de lo que estás editando. Antes de mergear,
suite entera.
