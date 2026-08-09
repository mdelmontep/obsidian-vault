---
title: una afirmación repetida no es una verificación
date: 2026-08-09
source: claude-code-session
tags: [metodo, seguridad, code-review]
---

La cookie de sesión de TuCRMIA **no era `HttpOnly`** durante toda la vida del proyecto, y llevaba
dentro `access_token` y `refresh_token`. Lo que lo mantuvo invisible no fue el descuido: fueron
**cuatro comentarios del repositorio afirmando que sí lo era**. El razonamiento era correcto
—canjear en el servidor— y la conclusión falsa: canjear en el servidor decide QUIÉN escribe la
cookie, no CON QUÉ MARCAS.

Cuatro copias de la misma frase **impiden** que alguien vaya a comprobarla: parece verificada por
repetición.

En la misma sesión salieron cinco de la misma familia: el tablero publicándose contra una URL
muerta (404 se ve igual que republicar), un contador antiabuso enchufado donde el atacante no
pasa, una migración que explicaba su ámbito en prosa sin el marcador que el guard lee, y nombres
de función repetidos en comentarios fuera de su módulo dueño.

**Regla**: al leer un comentario que afirma una propiedad de seguridad, la pregunta no es «¿es
razonable?» sino **«¿qué la comprueba?»**. Si la respuesta es otro comentario, no hay nada.
