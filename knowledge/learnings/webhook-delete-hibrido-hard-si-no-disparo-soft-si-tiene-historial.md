---
title: webhook delete híbrido — hard si no disparó, soft si tiene historial
date: 2026-05-02
source: claude-code-session
tags: [webhooks, ux, disenio-api]
---

Patrón para "eliminar" endpoints de webhook (o cualquier recurso con secret cifrado y deliveries asociadas):

- Si `count(deliveries WHERE endpoint_id = id) == 0` → `DELETE` real de la fila. Limpia errores de tipeo, webhooks de prueba, configuraciones equivocadas sin dejar restos en BD.
- Si `count >= 1` → soft-delete (`revoked_at = now()`, `active = false`). Conserva el secret cifrado para verificar firmas históricas si el cliente reclama una entrega.

UI: un solo botón "Eliminar" (icono papelera). El server decide qué hacer y devuelve `{ action: 'deleted' | 'revoked' }`. Ocultar revocados por defecto en el listado, con toggle "Ver revocados" cuando existen.

Evita la dicotomía mala "borrar de verdad pierde auditoría" vs "todo soft-delete genera basura visible". Auditoría se conserva donde importa, limpieza queda donde no.
