---
title: una decisión con efecto no puede depender solo del tipo que lee el llm
date: 2026-10-10
source: facturaia (#3121, #3310)
tags: [ocr, llm, clasificacion]
---
Dos fotos del mismo albarán, distintas solo en el brillo, salieron una como «albarán firmado» y otra como «albarán de compra». La segunda creó un albarán de compra de la org a sí misma.

- El tipo que devuelve el lector es estable con documentos claros, no entre tipos que se parecen. Si de él depende crear o registrar algo, falla sin avisar.
- Fix: una señal determinista decide (QR propio, o NIF propio MÁS número existente; el NIF solo no basta porque el nuestro también sale impreso como cliente). Con la señal, a revisión humana, nunca auto.
- Para probar la idempotencia, reenviar el mismo fichero no vale: lo frena el `file_hash` antes del OCR. Hace falta una variante, por ejemplo con otro brillo (sharp `modulate`).

Relacionado: [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]]
