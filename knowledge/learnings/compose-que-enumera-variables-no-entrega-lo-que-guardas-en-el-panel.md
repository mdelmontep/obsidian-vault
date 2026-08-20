---
title: un compose que enumera variables bajo environment ignora lo que guardas en el panel de Dokploy
date: 2026-08-20
source: facturaia
tags: [dokploy, docker, compose, secretos, observabilidad]
---
Si el `docker-compose.yml` **enumera** las variables bajo `environment:` en vez de usar `env_file`, lo que no está en esa lista NO llega al contenedor por mucho que esté guardado en el panel. Guardar el secreto y redesplegar da sensación de hecho y no hace nada.

Dos víctimas la **misma noche** del 19→20-ago-2026 en TuFacturaIA (`b40a1db9a` 00:54 y `5789f4dbc` 02:01), la segunda con la entrada de WhatsApp caída **ocho días** sin que saltara nada.

- **El síntoma nunca se parece a la causa**: sin el secreto de Meta, la verificación de firma da false y el receptor descarta cada mensaje **respondiendo 200**, con un `console.warn` como único rastro. Sin las claves de PII, el cifrado degrada a propósito y sigue escribiendo plaintext. Nada se rompe visiblemente.
- **No se audita por SQL**: el env del panel está cifrado en reposo, así que `where env like '%VAR%'` en la BD de Dokploy grepea ciphertext y siempre da falso negativo. Escribirlo por SQL es peor: un `UPDATE` así tiró producción 12 minutos.
- **Lo que sí vale**: `docker exec <c> env | grep -c '^VAR='` y después una sonda funcional con valor bueno contra valor malo, lanzada DENTRO del contenedor para no imprimir el secreto.
- Filo al escribir un guard: una variable puede estar declarada **con valor vacío** a propósito si el código hace `|| 'default'`. Lo que hay que comprobar es que esté DECLARADA en el compose; el valor es cosa del panel.

El cierre de la clase es un trinquete que compare los `process.env.X` del bundle contra la lista `environment:`.
Relacionado: [[docker-infra]] · [[facturaia]]
