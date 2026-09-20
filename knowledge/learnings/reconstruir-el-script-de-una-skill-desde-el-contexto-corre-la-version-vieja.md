---
title: reconstruir el script de una skill desde el contexto corre la versión vieja
date: 2026-09-20
source: facturaia
tags: [claude-code, skills, worktrees, arnes, verificacion]
---

El cuerpo de una skill llega inyectado en contexto **desde el checkout donde
arrancó la sesión**. Si ese checkout va por detrás, lo inyectado es la versión
vieja — y como se lee igual de autorizado que el disco, un script que se
reconstruye a partir de él corre **sin los arreglos que ya existen**.

Caso (`/fia-cierre`, 20-sep): el checkout principal iba 310 commits por detrás,
así que se inyectó la skill SIN el umbral de sustancia del issue #2532. Copié ese
script al `Workflow` y una dimensión devolvió relleno (`summary: "test"`,
hallazgo `"t"/"t"`) sin que nada la rechazara. El umbral existía desde hacía
trece días: `0` apariciones de `UMBRAL_RESUMEN` en el fichero del checkout, `7`
en `origin/main`. Diagnostiqué «regresión del arnés» y era mío.

El tell y el fix:

- Un issue **cerrado** que describe exactamente tu síntoma casi nunca es una
  regresión: primero comprueba si estás corriendo el fichero arreglado.
- Cuenta el símbolo del arreglo en las dos versiones, no lo supongas:
  `git show origin/main:<ruta> | grep -c <SIMBOLO>` contra el del checkout.
- Si vas a ejecutar el script de una skill, sácalo de `origin/main` o del
  worktree en la punta, nunca del cuerpo que te llegó inyectado.

Es el corolario ejecutable de «mi contexto no es el disco»: ahí la regla era no
AFIRMAR qué dice un fichero; aquí es no EJECUTARLO de memoria.
Ver [[cp-entre-checkouts-hereda-el-atraso]] · [[el-prompt-no-es-fuente-de-verdad-del-repo]]
