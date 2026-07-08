---
title: un gate agéntico/ml que no dispara suele estar inanido en el origen, no mal calibrado
date: 2026-07-08
source: claude-code-session
tags: [agentic, observabilidad, ocr, facturaia]
---
Sistema shadow→gate (auto-aprobación OCR de FacturaIA) llevaba 0 decisiones "verde" → el gate (≥50 verdes/30d, acierto ≥95%) nunca podía abrir. Reflejo natural: bajar el umbral de "proveedor de confianza" o backfillear su contador (`facturas_ok`).

Dry-run contra prod ANTES de escribir la migración: el backfill maduraba **0 proveedores** y bajar el umbral 3→2 tampoco (solo 3 proveedores con ≥2 recibidas limpias). Motivo real: el histórico limpio no existe — **86% de recibidas en `sin_aprobar`** (nunca aprobadas por el humano). La inanición está en el ORIGEN (faltan aprobaciones), no en el algoritmo ni el umbral.

Patrón: antes de tocar el umbral de un gate que "no aprende", mide con datos reales dónde muere el embudo — funnel de zonas + **distribución de motivos bloqueantes** + volumen de la señal que alimenta la maduración. Un backfill no madura nada si los datos base no existen. El dry-run ahorró una migración de efecto cero. Ver [[aceptar-sugerencia-hitl-debe-cerrar-decision-o-el-gate-no-abre]].
