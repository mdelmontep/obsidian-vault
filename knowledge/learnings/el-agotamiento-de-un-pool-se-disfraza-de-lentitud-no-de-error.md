---
title: el agotamiento de un pool se disfraza de lentitud, y un tope de test menor que el margen del código no se cumple nunca
date: 2026-09-05
source: mandadm
tags: [postgres, testing, arnes, concurrencia]
---
Dos corridas del MISMO gate sobre el MISMO árbol dieron rojo con conjuntos **distintos** (4 tests a
5 s una, 2 hooks a 10 s la otra). Conjuntos distintos = no-determinismo, no defecto. El fichero
sospechoso, aislado contra un cluster propio y con la misma carga: 3 de 3 en verde.

Dos causas, las dos del arnés:

- **`pg.Pool` no falla cuando se queda sin hueco: ENCOLA el `connect()` sin límite.** Así que agotar
  `max_connections` (100 por defecto) no da «too many clients» —que señalaría la causa— sino un
  timeout indistinguible de código lento. Con N ficheros en paralelo × `max` del pool, se roza el
  tope sin verlo. Holgura explícita en el cluster de test.
- **Un tope de test/hook menor que el margen que declara el código bajo test no se cumple jamás.** El
  worker daba 15 s a su apagado; el `afterAll` que lo esperaba tenía los 10 s por defecto de vitest.
  Estructural, no mala suerte.

Antes de subir un tope: comprobar que **ninguna aserción depende de él** (las medidas de tiempo de
verdad usan marcas propias). Después: **volver a mutar** para ver que la suite sigue mordiendo — si
no, has cambiado un rojo falso por un verde falso. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
