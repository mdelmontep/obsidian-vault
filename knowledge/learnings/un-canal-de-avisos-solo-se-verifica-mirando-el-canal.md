---
title: un canal de avisos solo se verifica mirando el canal, no el estado de la ejecución
date: 2026-08-12
source: claude-code-session
tags: [observabilidad, n8n, slack, metodo, anti-patron]
---
Monté el aviso de errores de Elphis a Slack, verifiqué **nueve** cosas por API —nodos,
credencial, conexiones, posiciones— y todas en verde. Disparé un error de prueba: el handler
ejecutó en `success`. **El mensaje no existía.** Lo vi al leer el canal, no antes.

Tres capas que lo taparon, y las tres son reutilizables:
1. **`onError: continueRegularOutput` en el nodo que ES la alerta.** Convierte «no avisé» en
   verde. En un nodo de notificación nunca: que rompa y se vea.
2. **Slack devuelve HTTP 200 con `{"ok":false,...}`** cuando rechaza el mensaje, así que el
   nodo HTTP lo da por bueno. Igual Meta y media API moderna: si el error viaja en el cuerpo,
   el código de estado no prueba entrega. Hace falta un nodo que exija `ok === true` y lance.
3. **Verificar el cableado no es verificar el efecto.** Mis checks probaban que el mensaje
   estaba bien enchufado, no que saliera.

Regla: un canal de aviso no está montado hasta que alguien LEE el aviso en su destino. Y el
gate del montaje es esa lectura, no el `success` de la ejecución.
Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
