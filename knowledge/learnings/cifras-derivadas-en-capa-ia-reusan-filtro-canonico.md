---
title: cifras de negocio en una capa nueva (ia/copiloto) deben reusar el filtro canónico, no reimplementarlo
date: 2026-05-27
source: claude-code-session
tags: [arquitectura, ia, datos, facturaia]
---
Al añadir una capa que devuelve cifras YA existentes (copiloto/IA, export, widget, voz), NO reimplementes el cálculo: reusa la constante/helper canónico de la fuente.

Caso TuFacturaIA: las tools del copiloto `getKPIs` y `getDeudaPorCliente` reimplementaban el filtro de "deuda por cobrar" más laxo que `cobros/aging` (les faltaba `tipo_documento='factura'` + `factura_origen_id IS NULL`). Un abono pendiente (total NEGATIVO, estado `pendiente`) entraba: `getKPIs` lo restaba, `getDeudaPorCliente` lo descartaba con `total<=0`, y ninguno coincidía con el dashboard. Cada tool daba un total distinto → divergencia = bug de confianza.

Fix: extraer el filtro a constante compartida (`DEUDA_ESTADOS_ABIERTOS` + columnas) y usarla en TODAS las queries (aging + las 2 tools). Regla: una cifra, una definición. Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].
