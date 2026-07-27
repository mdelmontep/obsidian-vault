---
title: escribir en una fuente y leer de otra hace que el agente niegue su propia escritura
date: 2026-07-27
source: claude-code-session
tags: [agentes-conversacionales, arquitectura, integraciones, single-source-of-truth]
---
Síntoma en una llamada real: «¿Qué reunión tengo con McDonald's?» → **«No me consta ninguna reunión con McDonald's»**, y cuatro turnos después el propio agente lista **dos** reuniones con ese cliente ese día.

Causa: la escritura y la lectura no compartían fuente. `meeting.schedule` crea el evento **solo en el calendario externo** (Graph) y no deja fila en la tabla del CRM (esa es de reuniones ya tenidas con resumen dictado); el read *por cliente* leía solo la tabla, mientras el read *por fecha* leía el calendario. Dos lecturas, dos fuentes, respuestas contradictorias.

**Patrón a vigilar** en cualquier agente con integraciones: por cada entidad, listar **dónde se escribe** y **desde dónde se lee cada pregunta posible**. Si una entidad vive en 2 sedes, toda lectura sobre ella debe consultar **la unión**, no una de las dos. Aquí la respuesta correcta no era sustituir una fuente por otra: lo agendado (calendario) va delante y el histórico (tabla) debajo, porque cada sede tiene datos que la otra no.

Corolario de diagnóstico: un «no me consta» **falso** es peor que un error visible — el comercial toma decisiones sobre la negación. Y ojo con la hipótesis fácil: aquí la primera sospecha («la fila quedó con un id de cliente equivocado») era **imposible**, no había fila que anclar. Verificar la hipótesis antes de arreglarla.

Relacionado: [[triggers-bd-sync-son-antipatron]] · [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]
