---
title: al reiniciar, reconciliar estado externo por clave natural — no cancelar+recrear
date: 2026-06-24
source: claude-code-session
tags: [arquitectura, integraciones, estado]
---
Servicio que trackea estado externo (posiciones de exchange, recursos cloud) con filas espejo en BD. Al reiniciar perdía el tracking en memoria → cancelaba TODAS las filas OPEN y las readoptaba desde la fuente externa.

Síntomas: una fila CANCELLED por cada redeploy (avalancha que ensucia listados/stats) + pérdida de datos que la fuente externa no devuelve (p.ej. SL/TP de la orden, que el exchange no expone tras adoptar).

Fix: reconciliar, no recrear. Cargar filas OPEN de BD, indexar por clave natural (par/símbolo/recurso). Para cada estado real: re-trackear la fila existente preservando su id y sus campos locales (SL/TP). Cancelar solo filas sin estado real o duplicados del mismo par. Crear fila nueva solo si hay estado real sin fila previa.

Aplica a cualquier reconciliación tras caída de un servicio stateful. Relacionado: [[boton-hitl-referenciar-estado-persistido-no-id-efimero-proveedor]]
