---
title: el reloj de la vm de colima oscila; un test que compara host y bd tolera, no se corrige el reloj
date: 2026-10-01
source: facturaia, agh-iberica
tags: [colima, docker, tests, flaky, tiempo]
---
Postgres dentro de Colima no comparte reloj con el Mac. Medido el 1-oct: Mac ~110 ms atrasado
contra time.apple.com y la VM ~80 ms por delante del host; tras `sntp` en el host y `date -s`
en la VM quedó a pocos ms, pero el NTP de la VM tiene jitter de decenas de ms (+3 a +166).

Un test que corta por `now()` de la BD frente a `Date.now()` del host cae de forma
intermitente y también en main limpio, lo que parece un fallo de la rama.

Medir: `docker exec <db> psql -Atc "select extract(epoch from clock_timestamp())"` entre dos
lecturas del host; si la hora de la BD supera la lectura POSTERIOR del host, la VM va adelantada.

Fix: que el test tolere ~200 ms o fije el corte a futuro (agh #2169, 4/4 verde con 26-141 ms).
Sincronizar relojes es puntual y vuelve a abrirse.
