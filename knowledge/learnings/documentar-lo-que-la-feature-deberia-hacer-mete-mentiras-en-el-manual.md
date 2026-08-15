---
title: documentar lo que la feature debería hacer mete mentiras en el manual
date: 2026-08-15
source: claude-code-session
tags: [metodo, documentacion, verificacion]
---

Escribiendo el manual de cinco correos nuevos que yo mismo acababa de mergear,
afirmé dos cosas en el mismo párrafo: que dejaban aviso en la campanita y que se
regían por Ajustes → Notificaciones. **Las dos falsas.** Ninguno llama a
`notify()`, y la lista de no-silenciables gobierna la campanita, no el copy de
email. No lo inventé: lo deduje del diseño, que es peor, porque suena coherente.

El manual es lo único que el cliente lee. Una frase de más ahí no es un comentario
optimista: es soporte contestando «pues debería llegarte a la campanita».

**Comprobación, siempre la misma**: para cada canal que prometas, grep del emisor
real (`notify(`, `sendEmail(`, el cron que dispara) en los ficheros de la feature.
Si el grep da 0, ese canal no existe. Cuesta un minuto y ya me ahorró dos errores
en un párrafo.

Efecto lateral que compensa: el grep destapó un hueco de producto real — cinco
avisos de dinero sin respaldo en campanita, así que un correo perdido es silencio
total.

Relacionado: [[escribir-la-doc-de-exportacion-de-un-sistema-lo-audita-entero]] · [[una-suite-en-verde-no-prueba-el-camino-real]]
