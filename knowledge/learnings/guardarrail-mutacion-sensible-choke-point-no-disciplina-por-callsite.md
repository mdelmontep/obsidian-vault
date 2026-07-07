---
title: guardarraíl de mutación sensible = un choke-point obligatorio, no disciplina por call site
date: 2026-07-07
source: claude-code-session
tags: [arquitectura, seguridad, patron]
---
Cuando una mutación puede repetirse desde varios sitios futuros (distintos providers/endpoints) y TODAS las instancias deben pasar por una verificación + registro (límite de gasto, permiso, auditoría), no confíes en que cada call site recuerde llamar a las 3 funciones en orden — un desarrollador (o tú mismo en 2 meses) se olvidará una vez.

Fix: una única función `runGuardedMutation({ ...params, mutate })` que internamente hace `assertLimit() → mutate() → logAudit()` y es el ÚNICO camino sancionado para ejecutar la mutación. Los call sites nuevos (ej. Meta Ads reusando el guardarraíl ya construido para Google Ads) llaman esta función, no la API externa directamente — así "ninguna mutación sin guardarraíl" es una garantía estructural (deep module, interfaz estrecha) en vez de una convención que hay que acordarse de seguir.

Caso real: `runGuardedMutation` en `src/lib/marketing/guardrails.ts` (facturaia, módulo Marketing/Growth) — reusado por Google Ads y Meta Ads sin duplicar la lógica de límite de presupuesto/audit log.
