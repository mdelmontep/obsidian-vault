---
title: una auditoría que acaba pidiendo permiso para un dato debe comprobar que no lo tiene ya
date: 2026-08-05
source: claude-code-session
tags: [metodo, auditoria, observabilidad, langfuse]
---
«Para saber esto haría falta activar X» es una **premisa**, no una conclusión: medirla antes de
escalarla. Escalar una premisa falsa gasta la decisión de otra persona y deja la pregunta sin
contestar.

Caso real (agh-iberica #747, **dos veces**): pidió *activar el tracing de contenido*, que llevaba
activo desde julio (`LANGFUSE_TRACE_CONTENT=true`, leído del container). El error: en Langfuse el
**texto vive en `traces.input`/`traces.output`, no en `observations`** — el EVENT por turno los trae
vacíos siempre (0 de 611 filas vs ~100 % en `traces`). Vio ceros en la tabla de al lado y concluyó
«apagado». Estaba a un `JOIN`.

- **Comprobar la premisa contra el sistema vivo**, no contra la memoria ni contra otra nota. Aquí:
  `printenv` en el container + un `count(*)` por tabla.
- **La raíz se arregla en el RUNBOOK, no en la nota de sesión.** La primera vez se anotó en el
  `status-log` y volvió a pasar 3 días después: nadie lee el histórico al arrancar una auditoría, el
  runbook sí. La frase culpable llevaba meses siendo cierta *antes* de un cambio de política.
- Una afirmación de doc con fecha implícita («las trazas no contienen texto del usuario») caduca sin
  avisar. Al leerla, preguntarse **desde cuándo** es verdad.
- Con el dato delante, la pregunta se contestó **en contra** de la hipótesis del auditor: 14 de 39
  pares SÍ repiten, pero solo **2** rachas de tres, una anterior al despliegue del breaker.
