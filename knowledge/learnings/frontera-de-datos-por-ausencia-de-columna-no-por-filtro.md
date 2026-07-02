---
title: frontera de datos (PII/compliance) = ausencia de columna, no filtro que se pueda olvidar
date: 2026-07-02
source: claude-code-session
tags: [compliance, pii, schema, seguridad, testing]
---

Cuando un módulo NO debe manejar cierto dato sensible (salario/SS/seguros en un agente comercial, PII fuera de su dominio), no lo filtres en la capa de salida — hazlo **estructural**: la columna/campo simplemente NO existe. Si no hay dónde guardarlo, no hay nada que filtrar ni fuga posible por un `select *` o un render olvidado.

**Refuerzos (defensa en capas):**
1. Tipo TS sin el campo + `CreateInput` sin él → no compila si alguien lo intenta pasar.
2. Executors mapean SOLO columnas nombradas explícitas — nunca `{...fields}` spread a un INSERT (un LLM podría colar `salario:45k` en `fields`).
3. **Test load-bearing**: introspección `information_schema.columns` que asierta el **conjunto EXACTO** de columnas (`toEqual([...])`, no `not.toContain`). Una migración futura que añada `salary` **falla ruidosamente** — es la garantía real detrás del claim "estructural".

Ojo: sigue siendo texto libre (`title`, `skills[]`) donde el usuario puede dictar "salario 60k" — eso es input libre, no campo estructurado; el claim aplica al schema, no al contenido.

Distinto de proteger una columna que SÍ existe con guard de rol ([[columnas-regulatorias-requieren-guard-rol-trigger-no-solo-rls]]). Caso real: AGH Ibérica #8 (Consultor sin salario/SS).
