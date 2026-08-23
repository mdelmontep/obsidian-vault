---
title: un trinquete que mide por fichero absuelve al fichero que ya importa el helper
date: 2026-08-23
source: facturaia
tags: [trinquetes, tests, arnés, billing]
---
Al blindar «nadie lee la columna espejo en crudo, se lee por el helper», el test obvio
es por fichero: ¿este fichero importa `pickEffectiveBillingStatus`? Da verde en cuanto
haya **una** llamada, y deja pasar las otras lecturas del mismo fichero.

Caso real: `suspend-overdue/route.ts` ya usaba el helper en el filtro de fuera y su
re-chequeo anti-carrera, dentro del bucle, seguía leyendo `org.billing_status` a pelo.
Lo cazó un escáner **por ocurrencia**, no el subagente que auditó el área.

Patrón: anclar en la ocurrencia (`.from('organizations')`), abrir ventana hasta su
`.select(` y exigir el embed ahí mismo. Dos gotchas al escribirlo: el escáner debe ser
consciente de la tabla (si no, marca ficheros que leen otra tabla con el mismo nombre de
columna) y la ventana debe llegar más allá de la línea, porque un `.select()` partido en
varias líneas concatenadas mete el embed fuera de los primeros 300 chars → falso positivo.

Y el escáner se prueba al revés: un segundo caso le da un fragmento malo conocido y
comprueba que muerde. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
