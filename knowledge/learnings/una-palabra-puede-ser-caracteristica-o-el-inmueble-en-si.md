---
title: una palabra puede ser característica o el objeto buscado, y el buscador debe decidir cuál
date: 2026-09-07
source: simarro
tags: [busqueda, nlu, facetas]
---
En el buscador de viviendas «garaje» estaba en el diccionario de **características**
(piso con garaje) y en ningún sitio como **tipo de inmueble**. Quien pedía "un garaje"
o "una parcela" recibía pisos y chalets, marcados además como *coincidencia exacta* —
la etiqueta que decide si el CRM ancla esa vivienda al cliente.

El patrón: en toda faceta hay tokens que son adjetivo del objeto y sustantivo del
objeto a la vez (garaje, trastero, local, parcela). Hay que resolver por **contexto**,
no por diccionario: si el token aparece **sin** un tipo de vivienda nombrado, es lo que
se busca y hay que quitarlo de las características; si aparece con uno, es un extra.

Corolario de negocio: cuando el resultado correcto es "no tenemos nada así", decirlo
y ofrecer lo que sí hay, en vez de rellenar con lo que no se ha pedido.
