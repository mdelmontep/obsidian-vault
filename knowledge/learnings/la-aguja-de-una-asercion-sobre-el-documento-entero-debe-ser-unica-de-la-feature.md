---
title: la aguja de una aserción sobre el documento entero debe ser única de la feature
date: 2026-07-31
source: claude-code-session
tags: [testing, correctness, pdf]
---
Al probar que algo sale impreso en un documento (PDF, email, HTML), la tentación es
`expect(texto).toContain(nombreDelCliente)`. **No muerde**: el nombre del cliente ya sale
en el bloque del receptor, en la cabecera y en el pie. La aserción está satisfecha por
contenido que la feature no produjo.

Caso FacturaIA (ticket e5dc74e7): test de composición del saludo congelado en la factura.
Saboteando el resolutor (`textoSaludo: null`) el PDF salía **sin saludo** y
`toContain(nombreCliente)` seguía verde — el nombre venía del bloque "PARA". Lo que muerde
es la **frase entera resuelta**: `Estimado <cliente>, le remitimos la factura <num>…`.

Regla: elegir como aguja una cadena que **solo** pueda existir si el código bajo prueba
corrió. Si el documento ya contiene el dato por otra vía, el dato no sirve de aguja; sirve
la plantilla resuelta alrededor de él. Comprobarlo siempre con la mutación, no razonando.
Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] ·
[[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]]
