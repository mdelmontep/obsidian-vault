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
