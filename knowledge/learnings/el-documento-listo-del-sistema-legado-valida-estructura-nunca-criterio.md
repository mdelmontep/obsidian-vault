---
title: el documento «listo» del sistema legado valida estructura, nunca criterio
date: 2026-08-30
source: agh-iberica
tags: [migracion, contabilidad, fixtures, yooz]
---
Al portar a AGH de Yooz a TuFacturaIA, el único documento en estado «listo para exportar»
(DKV, base 2.033,48 €) parecía el fixture perfecto para el generador del `.TRA`. Su asiento
es **contablemente incorrecto**: carga la `129` (resultado del ejercicio) contra la `410` del
proveedor, porque la línea nunca se codificó y cayó en el «Alta automática» del sistema.

Un documento del sistema origen prueba **el formato** (posiciones, longitudes, orden de
líneas, encoding) y nada más. El criterio de negocio se prueba con un fixture sintético que
tú has codificado bien — aquí, gasto 629x + IVA 472 + tercero 410x + retención 4751.

Corolario de diagnóstico: un asiento así no es un bug del sistema origen, es la **prueba de
dónde está el cuello de botella real** del cliente. AGH no tenía un problema de herramienta;
tenía 39 de 46 facturas sin codificar. → [[facturaia-yooz-agh-migracion]]
