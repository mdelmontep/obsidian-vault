---
title: al añadir un rol nuevo a un clasificador LLM, revisa los bloques de contexto que ya presuponen un rol fijo
date: 2026-07-01
source: claude-code-session
tags: [llm, prompt-engineering, ocr]
---

Un bloque de contexto previo que afirma sin condición "esta empresa es SIEMPRE el receptor/cliente"
puede contradecir y bloquear silenciosamente un criterio de clasificación nuevo donde esa misma
empresa pasa a tener el rol opuesto (emisor).

Caso real: añadir `doc_type='presupuesto'` (la org emite, no recibe) a un clasificador OCR que ya
tenía un bloque `CONTEXTO_RECEPTOR` fijo ("esta empresa es el CLIENTE/RECEPTOR") — el criterio nuevo
era correcto pero el bloque previo lo pisaba. Condicionar el bloque (explicitar la excepción) ayudó
pero NO bastó del todo: contra un documento de prueba sintético (sin membrete/logo real), el modelo
siguió clasificando por la forma estructural (tabla+IVA+total = factura) por encima del texto literal
de la cabecera ("PRESUPUESTO"), incluso con un ancla léxica explícita en el prompt.

**Fix/patrón**: al añadir un rol/tipo nuevo, grep TODOS los bloques de contexto fijo del prompt antes
de tocar solo la lista de clasificación. Y no confiar en un fixture sintético plano como prueba de
fiabilidad — la fuerte prior estructural del modelo puede dominar sobre instrucciones de texto;
validar con documentos reales (con logo/maquetación) antes de confiar en la clasificación.
