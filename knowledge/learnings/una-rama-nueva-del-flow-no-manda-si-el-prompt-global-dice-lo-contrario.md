---
title: una rama nueva del flow no manda si el prompt global dice lo contrario
date: 2026-09-07
source: simarro
tags: [retell, voz, conversation-flow, prompting]
---
Se añadió a un Conversation Flow de Retell el nodo que faltaba para el caso «la
reserva no se hizo», con sus seis salidas. Habría seguido fallando igual: el
`global_prompt` llevaba una línea que ordenaba, **tras cualquier `Reservar`**, leer
`confirmation_text` y añadir "un agente te contactará para confirmar los detalles".
El global aplica en todos los nodos, así que el agente decía el motivo del fallo y a
continuación prometía la cita inexistente.

Al añadir una rama a un flow, `grep` del `global_prompt` con el nombre de la tool
**antes** de dar el fallo por cerrado; si la instrucción global no distingue éxito de
fallo, partirla en dos líneas por resultado. Y el **orden de los edges importa**: la
condición del caso nuevo va primero, o la vieja se la come.

Ver [[repetir-una-instruccion-en-el-prompt-global-y-en-el-nodo-la-ejecuta-dos-veces]].
