---
title: 3 agentes paralelos auditando cambios grandes — security / backend / frontend
date: 2026-05-11
source: claude-code-session
tags: [workflow, claude-agents, code-review]
---

Antes de aplicar cambios grandes (>5 archivos, migración BD, gate de seguridad, infra nueva), spawn 3 agentes simultáneos con expertise distinta:

1. **Security audit**: auth, RLS, inyección, fuga cross-tenant, billing gates, prompt injection, secrets en logs
2. **Backend / DB audit**: triggers, race conditions, integridad referencial, índices, transacciones, performance, coexistencia con triggers existentes
3. **Frontend / UX audit**: a11y, estados vacíos, edge cases, persistencia de cambios, hooks order, layout shifts

**2 rondas** si la sesión tiene 2 bloques independientes (ej: módulos + cron). Cada ronda audita solo el código nuevo de su bloque.

**Filtrar falsos positivos visibles al user** con justificación documentada — NO aplicar todo lo que un agente diga. Los agentes suelen ser conservadores y proponen fixes innecesarios o regresivos.

**Caso real FacturaIA**: 2 rondas × 3 agentes = 6 reports auditando módulos IA + gate copiloto + cron. Hallazgos: 1 P0 (`save()` sin error handling) + 3 P1 (gate ausente, evento sin gate, cron secuencial timeout) + 2 P2 (índice faltante, dedupe orden). Falsos positivos descartados: thread_id cross-tenant (RLS ya aislaba), 9 vs 3 meses cashflow (lectura errónea del agente), service-key scope (preexistente fuera de scope), info leak en toast (mensajes ya diseñados para mostrarse). ~50% del total.

**Patrón clave**: el agente reduce el coste cognitivo de revisar tu propio código, no lo sustituye. La criba humana sigue siendo necesaria.

**Patrón orquestación "olas multi-agente con fix-consolidation" (Centro Fiscal 2026-05-22)**: estructura validada para módulo completo (~50 archivos, 3 migs SQL, frontend+backend+integración). Wave 0 revisión 5 expertises antes de tocar código → Wave 1 verificación fuentes oficiales (BOE/AEAT/etc) → Wave 2 implementación paralela (5-8 agentes) → Wave 1.5 fix-consolidation cross-agente (resuelve desalineamientos antes de propagar) → Wave 3 auditoría cruzada (seguridad + correctness + integración E2E) → Wave 2.6 fix bloqueantes auditoría → Wave 2.7 wiring final UI↔API. Cada fix-consolidation evita propagar bugs a la siguiente ola. Total ~15 agentes en sesión, 129 tests pass al cierre.

**Patrón cascada "3 planning + 1 bug-hunter cross-plan + 2 audit post-impl" (Sprint formulario facturas FacturaIA 2026-05-24)**: ligero comparado con olas, ideal para sprint de 6-12h en area acotada. 3 agentes planning paralelos con expertises ortogonales (ej: frontend / backend-DB / fiscal-legal) producen 3 planes contrastados → 1 bug-hunter cross-plan recibe los 3 outputs como input, detecta conflictos directos, gaps no contemplados, race conditions, regresiones potenciales → consolidación humana → impl → 2 audit post-impl paralelos (security/correctness y frontend/a11y/visual). El bug-hunter cross-plan es la pieza nueva: encuentra cosas que ningún plan individual ve. Caso real: backend reveló que columnas asumidas como "a crear" ya existían en BD (ahorro 6h migración); audit post-impl detectó bug fiscal voice (validación exención solo dentro de `if isFactura`) silente en tests. Total 6 agentes, 1227/1227 tests verde al cierre.
