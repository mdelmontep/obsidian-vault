---
title: si el canal obligatorio se cae, el aviso va al artefacto que sí acepta escritura
date: 2026-09-15
source: agh-iberica
tags: [proceso, slack, harness, coordinacion]
---
El protocolo de AGH exige anunciar y cerrar cada PR en `#cli-agh-iberica`. El 15-sep
`slack_send_message` empezó a devolver `no_text` con CUALQUIER texto —también con uno
de 21 caracteres— después de cuatro envíos correctos en la misma sesión; `slack_read_channel`
seguía funcionando. Descartado por bisección: no era longitud, mrkdwn, enlaces `<url|txt>`,
comillas ni caracteres no ASCII.

Lo que importa no es el fallo, es qué hacer: el aviso redactado **no se tira ni se deja
en el transcript**. Va como comentario en la propia PR, marcado «pendiente de enviar al
canal», y el prompt de la sesión siguiente lo nombra como primer paso. Así el ciclo queda
recuperable por alguien que no estuvo.

Regla de parada: 2-3 intentos y un texto trivial para discriminar herramienta vs contenido.
Insistir con el mensaje largo confirma lo mismo y cuesta una llamada cada vez.

Ver [[un-artifact-compartido-se-lee-pero-nunca-se-escribe]].
