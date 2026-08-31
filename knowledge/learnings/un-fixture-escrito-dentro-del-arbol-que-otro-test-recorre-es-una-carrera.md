---
title: un fixture escrito dentro del árbol que otro test recorre es una carrera
date: 2026-08-31
source: facturaia
tags: [testing, vitest, trinquetes, flaky]
---

Un test que prueba su trinquete **al revés** suele escribir un fichero de
mentira **dentro del árbol vigilado** — es la única forma de que el trinquete lo
vea. Y cualquier otro test que **recorra ese árbol** lo listará y luego intentará
leerlo. Vitest corre los ficheros de test en paralelo: entre el `readdirSync` y
el `readFileSync`, el escritor ya lo borró. `ENOENT`.

Se manifiesta de la peor forma posible: **rojo en el pre-push con el gate verde
minutos antes**, así que parece regresión del que empuja y no lo es.

Fix: el que recorre descarta el directorio **por nombre y ANTES del `statSync`**.
Descartarlo después deja la carrera viva un escalón más arriba — el `stat` falla
igual. No pierde dientes: sembrando el fixture a mano y quitando la exclusión,
`mutate` da ✓ VÍCTIMA.

Corolario al buscar: no basta con arreglar el lector que mordió. El mismo
escritor suele dejar fixtures en varios árboles (en FacturaIA, también un `.sql`
en `supabase/migrations/`), y cada árbol tiene sus propios recorredores.

**El corolario se cobró su pieza el mismo día** (el `.sql` de
`supabase/migrations/`, que leen 52 ficheros de test) y ahí la palanca fue la
CONTRARIA: mover al **escritor**, no excluir en 52 lectores. Elige por número —
excluye en el lector si son pocos y el fixture debe vivir en el árbol real; mueve
al escritor si el escáner ya acepta la ruta por parámetro. Nunca «es flaky».

Relacionado: [[el-entorno-de-un-test-que-evalua-sql-emitido-no-se-escribe-a-mano]]
