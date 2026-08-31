---
title: un estado sin caducidad es una promesa permanente en la pantalla del cliente
date: 2026-08-31
source: facturaia
tags: [ux, maquinas-de-estado, psd2, datos-huerfanos]
---
El estado que **no tiene salida por tiempo** acaba siendo mentira en pantalla.
Caso: `bank_consents.status='pending'` pintaba «Conectando…» sin caducidad; dos
clientes reales llevaban semanas viéndolo, uno siete.

Arreglar el origen no basta. Cerré la vía que dejaba el consent huérfano, pero
queda otra que ningún arreglo de servidor cubre: que el cliente abandone la
pantalla del banco. El estado transitorio se produce por diseño.

**Patrón**: deriva el estado de la EDAD en el render, como el vecino ya derivaba
«Caducada» de su `expires_at`. Las filas viejas se pintan solas bien, y eso
convierte un arreglo de datos en un arreglo de código.

**Mide el impacto en la capa que ve el cliente, no en la primera que se te
ocurra**: lo bajé a "ruido" porque la cuota solo cuenta los `active`. Cierto e
irrelevante — la lista devuelve todo menos `revoked`.
