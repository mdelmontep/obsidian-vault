---
title: la KB del proveedor y tu propio RAG son dos fuentes y hay que corregir las dos
date: 2026-09-10
source: laserys-las-rozas
tags: [retell, rag, pgvector, agentes-voz, knowledge-base]
---

Un agente de voz suele tener **dos** almacenes de conocimiento que nadie relaciona:

- La **KB del proveedor** (Retell `knowledge_base_ids` + `kb_config`), que se inyecta en **cada
  turno** y compite con el system prompt en igualdad de condiciones.
- El **RAG propio** (pgvector en Supabase) que consulta una tool tipo `consultar_precios`.

Corregir una no arregla la otra, y la contradicción que oye el cliente puede venir de cualquiera de
las dos. Antes de culpar al prompt de una "alucinación", busca el dato literal en ambas: teléfonos,
financiación y promociones viejas salían de un PDF subido cinco meses antes.

Y en el RAG: **cambiar el `content` de una fila sin volver a embeber no cambia lo que se recupera**
— la búsqueda sigue casando contra el vector del texto viejo. Regla para las dos: lo que el prompt
legisla, la base lo repite igual o no lo dice. Ver
[[recall-semantico-sin-umbral-es-confidently-wrong]] ·
[[retell-knowledge-base-api-requiere-multipart-form-data]].
