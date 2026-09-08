---
title: deducir el offset horario del número de mes desfasa una hora dos semanas al año
date: 2026-09-07
source: simarro, clinica-zen
tags: [fechas, dst, n8n, calendario]
---
`const offset = (mes >= 2 && mes <= 9) ? '+02:00' : '+01:00'` parece razonable y es
falso: el DST entra el **último domingo** de marzo y sale el último de octubre, así
que del 1 de marzo al cambio y del cambio al 31 de octubre la cita se escribe con
**una hora de desfase** en Kommo y en Calendar. Ningún test que corra en mayo lo ve.
3 nodos en Simarro, 4 en Clínica Zen (~34 días/año de citas una hora antes); se
encontró por `grep` de `getMonth()`, no leyendo el nodo ya sospechoso.

El offset se pide a la plataforma, no se calcula:
`Intl.DateTimeFormat('en-US',{timeZone:'Europe/Madrid',timeZoneName:'longOffset'})`.
Una hora de pared no lleva offset → dos pasadas (quedarse con el candidato que
cumple `offAt(wall - o) === o`; en la ambigua de octubre gana el mayor, en la
inexistente de marzo el menor).

**Calculado a mano, el umbral va en hora LOCAL**: el cambio es a las 01:00 UTC =
**02:00 locales en marzo y 03:00 en octubre**, así que comparar hora local contra el
instante UTC desplaza la frontera una hora. Lo cazó una mutación que **sobrevivió
siendo más correcta que el original**: eso acusa al oráculo, no al mutante. El
válido: la cita debe caer, EN MADRID, a la hora que se le dijo al paciente.
