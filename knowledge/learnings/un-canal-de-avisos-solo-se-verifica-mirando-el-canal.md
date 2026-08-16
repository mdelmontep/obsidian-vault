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

**El reverso, en el mismo canal (16-ago):** un aviso que salta **todos los días a la misma hora y se
resuelve solo** deja el canal tan inútil como si no llegara — se aprende a ignorarlo, y el día que
sale uno de verdad pasa desapercibido. Caso: el corte diario de Webempresa tumba un trigger IMAP a
las 06:0x y un watchdog lo levanta a las :20, sin nada que hacer por nadie. Se silencia **solo** ese
patrón (mismo workflow, mismo nodo, dentro de la ventana medida; fuera de ella avisa igual) y el
aviso se deja al componente que sabe si hubo que actuar — el watchdog, que avisa en rojo únicamente
si NO consigue repararlo. Silenciar ruido previsto no es perder cobertura si el escenario accionable
lo cubre otro; lo que hay que dejar anotado es la dependencia nueva (si el watchdog se para, ese
fallo ya no avisa) y que el evento se sigue registrando en `error_log`.

Ver [[ejecucion-en-verde-no-prueba-el-efecto]] · [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]]
