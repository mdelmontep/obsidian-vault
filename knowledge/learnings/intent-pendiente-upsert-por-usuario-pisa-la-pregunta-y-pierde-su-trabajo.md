---
title: un upsert de intent pendiente con PK por usuario pisa la pregunta y pierde su trabajo
date: 2026-08-25
source: facturaia
tags: [whatsapp, bots, hitl, idempotencia]
---
En un bot con preguntas pendientes (HITL) guardadas por upsert con PK = usuario/teléfono, la segunda
pregunta PISA a la primera; si la primera llevaba trabajo asociado (media subida a storage, payload
en cola), queda huérfano sin error: ya nada lo referencia. Caso real (facturaia #2183): foto →
«¿subo este documento?» → llega otra foto antes de contestar → el intent nuevo reemplazaba al vigente
y la 1ª foto moría en `_pending/` para siempre (18 huérfanos medidos en prod).
Fix: FUSIONAR los items del intent vigente en el nuevo (mismo tipo + no caducado + misma org), no
reemplazar; la pregunta se repite con el total («¿Subo estos 2 documentos?»).
Corolario: el cierre del lote debe HABLAR siempre que algo se descartó (duplicado idempotente, fallo,
corte por quota a mitad): «estoy leyendo 2» seguido de silencio se lee como pérdida. Y un corte
org-level a mitad de lote sale con `break` etiquetado, no con `return`, para no tragarse ese cierre.
