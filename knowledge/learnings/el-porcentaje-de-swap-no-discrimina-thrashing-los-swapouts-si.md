---
title: el porcentaje de swap no discrimina thrashing, los swapouts sí
date: 2026-08-31
source: facturaia
tags: [macos, rendimiento, agent-browser, arnes]
---
Criterio escrito para abrir olas de navegador: no abrir con el swap por encima del 50 % o
menos de 2 GB libres. Con el swap al 89 % el criterio dice que no, dos veces seguidas — y las
dos veces medía cosas distintas.

El porcentaje es un **proxy de estado**, no de actividad. Swap alto puede ser swap *asentado*
(se llenó hace horas, nadie lo toca) o thrashing vivo. Lo que discrimina es el caudal:

```bash
vm_stat | awk '/Swapouts/{print $NF}'   # dos lecturas separadas → tasa/s
```

`swapouts ≈ 0/s` = asentado, se puede abrir un navegador. Miles de `pageins`/s con swapouts
subiendo = thrashing, y ahí no se abre nada. Segunda vez: 4.163 pageins/8 s, y la causa era un
`next build` de una sesión paralela; en cuanto salió, desapareció.

El matiz **no relaja el criterio para una ola de 3-4 navegadores**, donde el 50 % sigue
mandando porque el pico llega después de medir. Vale para decidir si abres **uno**.

Corolario: antes de culpar a la máquina, `ps -Ao rss,pid,comm | sort -rn | head` — y si el que
come es el gate de otra sesión, se espera, no se mata.
