---
title: el resumen automático de una llamada viene en inglés — no lo pongas en un campo que ve el cliente
date: 2026-08-24
source: tecnocloud
tags: [retell, voz, i18n, ux]
---

`call_analysis.call_summary` de Retell llegó **en inglés en 12 de 12** llamadas reales de ago-2026
("The user requested a callback to phone number…"), con el agente hablando español y el prompt en
español. Quien resume no es el modelo de la conversación y su idioma no se configura desde ahí.

- La trampa es que suena a interno ("resumen automático") y acaba en el **asunto del ticket**, que
  sí ve el cliente: lista del portal, detalle, y la plantilla del acuse de creación por email.
- Regla: el texto que genera el proveedor va a la **nota interna**. Lo que ve el cliente lo compones
  tú — fecha y hora en `es-ES` con `Europe/Madrid` distingue igual en una lista de 25.
- Medir el idioma sobre **N llamadas reales**, no sobre una: con una sola no sabes si es el idioma
  del proveedor o casualidad del contenido.
- Mismo patrón en cualquier campo autogenerado que cruce el borde interno→cliente (transcripción,
  categoría, sentimiento). → [[etiqueta-de-estado-interno-se-tapa-en-el-where-no-en-el-render]]
