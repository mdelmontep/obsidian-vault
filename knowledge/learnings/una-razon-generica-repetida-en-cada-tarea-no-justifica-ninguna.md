---
title: una razón genérica repetida en cada tarea no justifica ninguna
date: 2026-09-06
source: mandadm
tags: [metodo, agentes, planificacion, verificacion]
---
En `ESTADO.md` casi todas las tareas de las fases B-G estaban en `doing` con la misma nota: «el
"hecho cuando" exige Instagram real». Suena a razón y cierra la pregunta, así que nadie la audita.
Lo delató un intento de sustituirla por posición: **la cadena casaba 9 veces en el fichero**. Al
comprobarlas una a una, cuatro tareas (C1, E2, F1, F7) no tocaban Instagram y estaban terminadas y
medidas; solo C4 tenía un motivo real, y era otro.

El defecto es de copia, no de contenido: un agente redacta la nota para la tarea donde sí aplica y
la arrastra a las vecinas. Una razón que vale para todas no discrimina, y esconde justo lo que ya
está hecho — es decir, trabajo terminado que nadie marca ni cobra.

**Fix, una línea:** antes de creerte un campo de estado, `grep -c` de su texto. Si el mismo motivo
aparece más de una vez, no es el motivo de ninguna: reverifícalas por separado. Y al escribirlo,
que la razón nombre algo propio de esa tarea (el endpoint, el permiso, el paso) o no sirve.
Ver [[una-afirmacion-repetida-no-es-una-verificacion]] · [[la-suposicion-de-un-agente-escrita-en-indicativo-se-lee-como-decision]] · [[un-commit-de-agente-con-un-hecho-falso-se-barre-entero]]
