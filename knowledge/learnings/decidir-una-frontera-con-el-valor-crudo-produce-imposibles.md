---
title: decidir una frontera con el valor crudo y redondear después produce imposibles
date: 2026-08-07
source: claude-code-session
tags: [formateo, redondeo, unidades, tests]
---

Al escribir un formateador de tiempo mordió dos veces el mismo error, y la
segunda vez después de haber comentado en el código que lo había evitado:

- Partir en horas y minutos ANTES de redondear: 5,9966 h → `5 h 60 min`.
- Elegir la rama con el valor crudo (`if (n * 60 < 1)`) y redondear DENTRO
  (`Math.round(n * 3600)`): 59,6 s → `60 s`.

**La regla**: redondea primero a la unidad más pequeña que vas a mostrar, y
decide TODAS las fronteras sobre ese entero. `const seg = Math.round(n * 3600)`
y a partir de ahí ya no vuelvas al valor original.

**Por qué los tests no lo cazaron**: probaban los extremos (59 y 60) y la banda
intermedia pasaba. Para un formateador con fronteras, el test que vale es un
barrido — «ninguna salida contiene `60 s`, `60 min` ni `h 60 min` en todo el
rango» — no una lista de casos elegidos a mano.

Relacionado: [[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
