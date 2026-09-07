---
title: deducir el offset horario del número de mes desfasa una hora dos semanas al año
date: 2026-09-07
source: simarro
tags: [fechas, dst, n8n, calendario]
---
`const offset = (mes >= 2 && mes <= 9) ? '+02:00' : '+01:00'` parece razonable y es
falso: en España el DST entra el **último domingo** de marzo y sale el último de
octubre, así que del 1 de marzo al cambio y del cambio al 31 de octubre la cita se
escribe con **una hora de desfase** en Kommo y en Google Calendar. No lo detecta
ningún test que corra en mayo. En Simarro estaba replicado en 3 nodos del mismo
workflow — el bug se encontró por `grep` de `getMonth()`, no por leer el nodo que ya
se sabía malo.

El offset real se pide a la plataforma, no se calcula:
`Intl.DateTimeFormat('en-US',{timeZone:'Europe/Madrid',timeZoneName:'longOffset'})`.
Ojo: una hora de pared no lleva offset, así que hay que resolverla en **dos pasadas**
(probar cada candidato y quedarse con el que cumple `offAt(wall - o) === o`); en la
hora ambigua de octubre gana el mayor, en la inexistente de marzo el menor.
