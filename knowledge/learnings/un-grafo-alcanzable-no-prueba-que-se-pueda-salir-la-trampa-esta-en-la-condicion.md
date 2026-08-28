---
title: un grafo alcanzable no prueba que se pueda salir, la trampa está en la condición
date: 2026-08-28
source: centro-elphis
tags: [retell, voz, conversation-flow, auditoria]
---
Un BFS de alcanzabilidad sobre las aristas de un flow dice «0 nodos atrapados» y aun así
el agente no sabe despedirse: el camino existe, pero **ninguna condición dispara con una
despedida**. La salida solo se abría avanzando por el embudo, así que a un «gracias, ya
está» el modelo seguía empujando a la cita. Hermano de
[[retell-la-condicion-del-edge-manda-sobre-el-prompt]]: allí la condición pedía de más,
aquí sencillamente no contempla el caso.

Auditar aristas es leer **condiciones**, no contar destinos. Pregunta por nodo: ¿qué dice
el usuario que hoy no encaja en ninguna salida?

Dos detalles al añadir la arista: (a) las aristas nuevas se **añaden al final**, porque el
orden es prioridad y una salida de despedida delante de las de crisis se las come; (b) la
condición tiene que excluir el falso positivo — «NO uses esta salida si solo está
contestando a una pregunta tuya». Con eso, las fugas de conversación pasaron de 3/21 a 0.
