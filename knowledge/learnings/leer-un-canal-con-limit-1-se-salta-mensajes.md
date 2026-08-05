---
title: leer un canal con limit=1 o filtro de fecha se salta mensajes recién llegados
date: 2026-08-06
source: claude-code-session
tags: [slack, mcp, metodo]
---
Dos veces en una noche: un compañero acababa de escribir y **leí el canal y no lo vi**, así que
respondí «no ha escrito nada» a una persona que lo tenía delante.

Las dos causas, y ninguna es un fallo del API:
- **`limit=1` devuelve el más reciente**, y si tu propio mensaje es posterior al suyo, el suyo no sale.
  Al ir publicando durante la sesión, tus mensajes tapan los ajenos.
- **un filtro `oldest=<ts>` excluye lo anterior a ese instante**, y el mensaje que buscas puede ser de
  unos minutos ANTES del tuyo.

**Cómo leer para decidir: `limit` de 4-5, formato detallado y SIN filtro de fecha.** El formato
detallado además trae el `Message TS` y el autor, que es lo que permite ordenar de verdad en vez de
fiarte de la posición.

Y el corolario general, que es el que duele: **«no aparece en mi lectura» no es «no ocurrió»**. Si
alguien te dice que hay algo, el sospechoso por defecto es tu consulta, no su memoria — mismo error que
truncar una salida y leer la ausencia como negativo.
