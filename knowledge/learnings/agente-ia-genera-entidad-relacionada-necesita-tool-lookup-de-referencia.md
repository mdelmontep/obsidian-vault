---
title: agente ia que genera entidad relacionada necesita tool de lookup de referencia
date: 2026-04-28
source: claude-code-session
tags: [n8n, ai-agent, tool-calling, design]
---

Cuando un AI agent crea una entidad que **referencia a otra existente** (abono → factura, reembolso → pago, rectificativa → original), debe tener una tool de lookup de la entidad origen y el prompt debe forzar su uso.

## Caso real (FacturaIA)

Agente generaba abono con `total: 0` y `factura_origen_id: null` cuando el usuario decía "abono de la factura A2026-0005". No tenía tool `consultar_facturas`, así que inventaba líneas vacías.

## Patrón

1. Tool `consultar_X` que devuelve las entidades referenciables (filtradas por org).
2. En el prompt: "Si tipo == ABONO, OBLIGATORIO llamar a consultar_X antes de devolver JSON".
3. Si no encuentra: el agente devuelve `{error: "no_encontrada", mensaje: "..."}` y el flujo posterior detecta el error y manda mensaje pidiendo el número exacto.
4. El endpoint receptor **rechaza explícitamente** si falta el `id` de origen (defensa en profundidad).

Es complementario al patrón de descripciones de tool no genéricas: aquí el problema NO es la descripción, es que la tool ni siquiera existía.
