---
title: pipeline async que solo notifica el camino feliz deja al usuario sin respuesta en el fallo
date: 2026-07-22
source: claude-code-session
tags: [whatsapp, ux, notificaciones, facturaia]
---
Caso real: cliente manda foto de ticket por WhatsApp, el OCR no logra leerla
(`noLegibleComoFactura`, estado `revisar`) y el flujo termina ahí — sin
mensaje al remitente. El único punto del código que enviaba WhatsApp era el
bloque de éxito (factura consolidada), 700+ líneas después del punto de
fallo. El cliente se queda sin saber que algo falló hasta que alguien revisa
la bandeja manualmente.

El ack inicial de encolado ("Recibido, estoy leyendo…") es neutro a
propósito (aún no se sabe el resultado) — eso hace más fácil olvidar que el
mensaje de CIERRE debe existir en TODAS las ramas de salida del pipeline, no
solo en la feliz. Un pipeline con N `return` tempranos necesita auditar cada
uno: ¿este exit deja al usuario sin cerrar el loop?

Al revisar/auditar un endpoint que dispara notificaciones de éxito, grep
todos los `return`/exit points tempranos y verificar cuáles SÍ tienen un
canal de vuelta al usuario y cuáles no. Aplica a cualquier canal (WhatsApp,
email, webhook saliente), no solo OCR.
