---
title: antes de preguntar al cliente, mira si el dato está en el sistema origen
date: 2026-08-02
source: claude-code-session
tags: [migraciones, clientes, metodo, facturaia]
---
En una migración desde un ERP viejo, tres veces en un día íbamos a pedirle a la
clienta datos que **ya teníamos** en su propio backup:

1. **85 precios**: el listado decía que faltaban a 105 artículos; faltaban a 20.
   `precio_lista_base` es derivada (`tarifa/unidad`) y un servicio propio no tiene
   tarifa: su precio vive en `precio_venta_calculado`. Una columna generada puede
   estar a 0 sin que falte el dato.
2. **Los nombres de artículo**: estaban en `materiales.descripcion` (1000 chars),
   campo que el primer volcado no trajo. El esquema se leyó del código ASP del
   backup, sin restaurar nada.
3. **Una pregunta que no existía**: «¿aplicamos el 78 % de este proveedor a estos
   1.306 artículos?». El descuento cuelga de (fabricante, familia, proveedor) y
   ese 78 % era de UN fabricante. El escenario alarmante salió de leer un volcado
   que ya había perdido una dimensión.

Regla: una pregunta al cliente sobre un **dato** es señal de que no has mirado el
origen; las preguntas legítimas son de **decisión**. Restaurar el backup (o leer su
código, que suele estar en claro) cuesta una tarde; un ciclo de preguntas cuesta
días y encima invita a teclear mal lo que ya tenías. Ver
[[columna-generada-stored-para-equivalente-derivado]].
