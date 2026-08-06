---
title: auditar un agente por sus trazas sin cruzar la BD no ve lo que dijo que hizo y no hizo
date: 2026-08-06
source: claude-code-session
tags: [langfuse, observabilidad, auditoria, agentes, metodo]
---
Leer solo las trazas (Langfuse, n8n executions) encuentra los turnos raros. **No encuentra
los fallos que consisten en que el agente diga «Listo» y la fila salga distinta o no salga.**
Ésos son diferencia entre `traces.output` y la base, y solo aparecen cruzando las dos.

Método: sacar cada acción con `status:"executed"` de la ventana y **contarla contra las filas
reales**. Dos discrepancias típicas, las dos mudas:

- **Ejecutadas sin fila de auditoría** → el write no está cableado al store de audit.
  (Caso real: 15 acciones ejecutadas, 11 filas en `audit_log`.)
- **Fila que existe con la FK a NULL** → el LLM no tenía campo por donde emitirla.
  (Caso real: toda tarea dictada con `client_id` NULL → invisible en TODA la UI, y el
  propio read del agente filtraba por esa columna que ningún write poblaba.)

Las dos dicen «hecho» en la traza y la entidad existe: un error-analysis que solo lee trazas
las declara sanas. Corolario barato: cuatro contadores SQL diarios (ejecutadas sin audit ·
FK nula · `errorClass` no vacío · rachas de clarify idénticos) encuentran esto sin gastar un
token. Ver [[una-columna-de-error-que-nadie-consulta]].
