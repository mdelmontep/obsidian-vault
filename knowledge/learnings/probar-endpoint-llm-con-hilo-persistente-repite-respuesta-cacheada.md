---
title: probar un endpoint de copiloto/LLM con hilo persistente puede repetir la respuesta anterior sin llamar tools
date: 2026-07-03
source: claude-code-session
tags: [testing, llm, copiloto, gotcha]
---
Al probar por API (curl firmado) un endpoint conversacional que persiste hilo por `(org, user)` — p. ej. el puente WhatsApp del copiloto, que reusa `copiloto_threads` con `titulo='WhatsApp'` — repetir la misma pregunta con el mismo `org_id`/`from_phone` puede hacer que el LLM **repita literalmente la respuesta anterior de memoria** (mismo token/enlace incluido) en vez de volver a invocar las tools, porque el historial del hilo ya contiene esa respuesta.

Sin verificar en BD, esto parece un éxito (respuesta con shape correcto) pero es un falso positivo: no se ejecutó nada nuevo.

Detección: comprobar en BD que la acción REAL ocurrió (ej. nueva fila en la tabla que la tool debería haber escrito) con timestamp posterior a la llamada de prueba.

Fix para forzar una llamada fresca sin tocar el código: renombrar temporalmente el `titulo` del hilo de esa combinación (org, user) en BD — el lookup no lo encuentra y crea uno nuevo en la siguiente llamada.
