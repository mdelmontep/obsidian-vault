---
title: un workflow que muere a mitad devuelve cero, y cero no significa limpio
date: 2026-08-10
source: claude-code-session
tags: [claude-code, harness, auditoria]
---
Una auditoría de N agentes en fases —buscar → refutar → sintetizar— se quedó sin sesión después de
buscar. Devolvió `{total: 124, sobreviven: 0, hallazgos: []}`.

**`sobreviven: 0` no significaba que nada sobreviviera: significaba que nadie llegó a juzgar.** Leído
del tirón es un informe de auditoría limpia, y es el falso verde más caro posible: cierra el tema.

Dos reglas que salen de esto:
- Un agregado de una fase POSTERIOR no se puede leer sin mirar cuántos agentes murieron. El resumen
  trae `agents_error`; si es >0, el agregado no vale.
- Los resultados intermedios están en `journal.jsonl` del run. **Recupéralos y persístelos a disco
  antes de diagnosticar nada**, con un aviso por delante de que no están refutados.

Y al pasar el alcance: una lista JSON llega como cadena y el guion la parte por comas dejando claves
con corchetes. Pasar la lista separada por comas, que es la forma que el propio medidor imprime.
Ver [[una-suite-en-verde-no-prueba-el-camino-real]]
