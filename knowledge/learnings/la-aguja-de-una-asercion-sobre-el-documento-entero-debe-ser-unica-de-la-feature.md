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

**Dos ocurrencias más al día siguiente** (cabos de la misma tanda), las dos cazadas por el
gate y no por mí: (1) un caso afirmaba `>1.234,50 €<` para probar el `@total@` de un texto
tipo, y ese patrón exacto lo produce **la píldora TOTAL del propio PDF** → seguía verde con
el texto tipo desactivado; (2) el test viejo de plantillas hacía `toContain('pre-wrap')` sobre
el documento entero, satisfecho por cualquier otro bloque. Salida barata: **envolver en
marcadores propios** (`'IMPORTE:@total@FIN'`) y afirmar solo sobre lo de en medio, o capturar
por regex el contenedor concreto.

Regla: elegir como aguja una cadena que **solo** pueda existir si el código bajo prueba
corrió. Si el documento ya contiene el dato por otra vía, el dato no sirve de aguja; sirve
la plantilla resuelta alrededor de él. Comprobarlo siempre con la mutación, no razonando.
Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] ·
[[mock-funcion-compartida-en-test-endpoint-falso-verde-composicion]] ·
[[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]]

**Misma trampa en un candado por texto sobre SQL (3-sep-2026, mig 819):** el test buscaba el predicado de la población (`f.total > 0`) en el fichero entero, y la verificación auto-abortante repite ese predicado; el mutante en la población seguía verde por la copia. Salida: acotar cada aserción a su bloque (`slice` entre `CREATE TEMP TABLE` y su `;`, y desde `DO $verificacion$`) y exigirla en los dos. Lo cazó `mutate`, no la lectura.
