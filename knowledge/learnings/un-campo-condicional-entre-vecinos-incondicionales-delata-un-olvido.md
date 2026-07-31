---
title: un campo condicional entre vecinos incondicionales delata un olvido, no una decisión
date: 2026-07-31
source: claude-code-session
tags: [correctness, code-review, heuristica]
---
Heurística de revisión barata y que hoy acertó **dos veces en el mismo día**: en
un bloque donde N campos hermanos se tratan igual, el que se trata distinto casi
nunca es intencionado. Si lo fuera, habría un comentario diciendo por qué.

Caso 1 (FacturaIA #1416, fuga de datos). `selectCliente` asignaba todos los
campos del cliente sin condición —`setClienteDireccion(c.direccion || '')`,
`setClienteEmpresa(c.empresa || '')`…— **menos el email**, que iba dentro de un
`if (c.email)` sin `else`. Al cambiar de un cliente con email a otro sin él, la
dirección del primero se quedaba pegada; con la casilla de enviar marcada por
defecto, la factura de B se iba al correo de A.

Caso 2 (#1415). En una plantilla PDF, tres bloques de texto libre llevaban
`whiteSpace: 'pre-wrap'` y un cuarto —con el mismo `padding`, `fontSize` y
`lineHeight`— no.

Corolario para el fix: **quitar la condición, no añadir el `else`**. Sin rama, el
fallo no puede volver por omisión; con `else`, el siguiente lo vuelve a olvidar.
Ver [[la-aguja-de-una-asercion-sobre-el-documento-entero-debe-ser-unica-de-la-feature]]
