---
title: un barrido de mutación que SALTA los tests relevantes dice "sin víctima" y parece cobertura ausente
date: 2026-09-05
source: mandadm
tags: [mutacion, testing, arnes, postgres]
---
`mutate` aborta con «ARNÉS ROTO» si el comando **no ejecutó tests**. No detecta el caso peor: que
ejecutara los irrelevantes. Muté la verificación de la firma HMAC para que siempre diera válida y el
barrido dijo `SIN VÍCTIMA` con «14 passed | 18 skipped» — los 18 saltados eran precisamente los que
necesitaban `DATABASE_URL`. Repetido con Postgres delante: control 32 passed, mutación 3 rojos. El
test estaba perfecto; el que medía cero era yo.

**Regla:** un `SIN VÍCTIMA` no se cree hasta mirar el **conteo de saltados** de la corrida de
control. Si hay skips, el barrido no ha medido esa protección — ha medido otra cosa y lo ha
presentado como cobertura que no existe.

**Arnés que lo evita:** un script que levanta el cluster UNA vez y reconstruye el esquema desde
`migrations/*.sql` **con glob, no con lista**, antes de cada suite. El glob es lo que hace que una
mutación en un `.sql` se mida de verdad, y lo que impide que una migración nueva quede fuera del
barrido sin que nadie se entere. Ver [[una-mutacion-que-produce-codigo-valido-no-demuestra-ningun-rojo]].
