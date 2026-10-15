---
title: un helper de test que devuelve un campo homónimo contamina la petición al esparcirlo
date: 2026-10-15
source: facturaia
tags: [tests, integracion, fixtures]
---
El helper `albaranEmitido()` devolvía `{ id, numero, ... }`, con `numero` como número del
**albarán**. Los casos hacían `rpc({ ...a, p_cantidad })` y el mapeo convertía `numero` en
`p_numero`, el número de la **reclamación**. Resultado: los casos «sin número» iban todos por
la rama «con número», y verdes. La rama que querían probar no se ejecutaba nunca.

Patrón: un fixture que se esparce (`...a`) en una llamada no debe devolver campos con el
nombre de un parámetro de esa llamada. Hay que nombrarlos por lo que son (`numeroAlbaran`)
o pasar los campos explícitos. Señal: un caso «sin X» que pasa sin tocar la rama de «sin X».
Para comprobarlo, mete un `throw` en esa rama y mira si algún caso se pone rojo.

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]].
