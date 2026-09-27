---
title: un check aplicado antes del merge deja al código viejo escribiendo contra él
date: 2026-09-27
source: facturaia
tags: [supabase, migraciones, deploy, check-constraint]
---
«Aplicar y verificar la migración ANTES de mergear» es correcto para columnas, funciones y CHECKs que amplían lo permitido. Para un CHECK que **estrecha** lo que se acepta, es al revés.

Caso (facturaia #3004, mig 956, 27-sep-2026): `clientes_nif_normalizado` exige el NIF sin guiones. Se aplicó a prod a las 15:15 y el código que normaliza antes de guardar se desplegó a las 15:21. Durante esos seis minutos, quien guardara un NIF con guion habría recibido un 23514, porque ningún trigger lo normaliza. No hay constancia de que le pasara a nadie, y eso fue suerte, no diseño.

Cómo se hace:
- Si el CHECK solo amplía (valor de enum nuevo, columna nullable), se aplica antes. Sin él, el código nuevo es el que falla.
- Si el CHECK estrecha, primero va el código que ya escribe el valor limpio, y el CHECK después, en otra migración. Otra opción es crearlo `NOT VALID` y validarlo tras el deploy.
- Si el CHECK va con backfill, antes de nada hay que medir en prod si quedan colisiones. Aquí había seis parejas de duplicados en orgs de prueba, y la migración habría abortado a mitad de camino.

Relacionado: [[aplicar-migraciones-a-prod-antes-del-merge-caduca-la-reserva-de-numero]] · [[enum-nuevo-en-codigo-sin-ampliar-check-bd-rompe-insert-silencioso]]
