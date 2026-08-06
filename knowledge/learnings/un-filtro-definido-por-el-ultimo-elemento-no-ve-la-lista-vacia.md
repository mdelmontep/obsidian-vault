---
title: un filtro definido por el último elemento no ve la lista vacía
date: 2026-08-06
source: claude-code-session
tags: [ux, bandejas, producto, sql, facturaia]
---
Una bandeja de soporte filtraba «sin contestar» por `ultimo_mensaje_autor = 'user'`. Suena
correcto y está mal en el borde: el ticket que **no tiene ningún mensaje** —el cliente lo abre
y nadie escribe— tiene ese campo a NULL, así que no entra en el filtro. Los que peor están son
justo los invisibles. En prod eran 7 de 8 tickets abiertos, con el estado vacío diciendo
«Nadie espera respuesta».

- Un predicado sobre «el último X» asume que **hay** X. Al escribirlo, preguntarse siempre qué
  devuelve con la colección vacía: casi siempre `NULL`, y `NULL` no cumple ninguna condición.
- El arreglo no es tocar ese filtro, es añadir el eje que faltaba: «¿hemos respondido alguna
  vez?» (existe algún mensaje público nuestro) es una pregunta distinta de «¿quién habló el
  último?», y la lista muda solo la contesta la primera.
- Señal de que pasa: un estado vacío que afirma algo tranquilizador («nada pendiente») mientras
  la lista completa tiene trabajo. El vacío de un filtro es un aserto sobre el mundo — si el
  filtro es incompleto, el copy miente con toda la confianza.

Ver [[facturaia]]
