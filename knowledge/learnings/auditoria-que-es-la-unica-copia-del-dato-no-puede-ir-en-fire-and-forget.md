---
title: si la auditoría es la única copia que quedará del dato, no puede ir en fire-and-forget
date: 2026-07-29
source: claude-code-session
tags: [observabilidad, auditoria, borrado, facturaia]
---

`void logSystemAction({...})` es el patrón correcto para auditar casi todo: la traza no
debe tumbar la acción. Pero cuando la acción BORRA el dato y el log guarda su contenido,
ese log deja de ser traza y pasa a ser el único backup — y `admin-audit.ts` hace
`catch { console.error }` sin relanzar, así que un insert fallido se lleva el texto para
siempre y solo queda un log efímero de contenedor.

Caso TuFacturaIA: borrar un mensaje del hilo de un ticket (`feedback.message.delete`)
guardaba el `cuerpo` en `admin_audit_log`… con `void`, y DESPUÉS del delete.

Fix, solo en ese endpoint: `await` la auditoría ANTES del borrado y responder 500 si no
entra ("no se ha podido dejar traza, así que no se borra"). El `void` se queda como está
en el resto del módulo — la excepción se justifica por ser la única copia, no por ser
un borrado.

Regla: al escribir un endpoint destructivo, preguntar "¿qué queda de este dato después?".
Si la respuesta es "la fila de auditoría", esa fila es parte de la transacción.
Ver [[fire-and-forget-resultado-descartado-esconde-fallo-loguear-en-transporte]] ·
[[fk-cascade-desde-tabla-de-auditoria-la-poda-borra-la-prueba]]
