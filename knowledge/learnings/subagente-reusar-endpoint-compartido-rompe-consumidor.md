---
title: subagente que reusa un endpoint compartido rompe el consumidor existente
date: 2026-06-27
source: claude-code-session
tags: [subagentes, api, refactor]
---
Un subagente, al construir un panel nuevo, reescribió un endpoint EXISTENTE
(`/api/admin/email-preview`: cambió auth propietario/admin → superadmin y el
shape del body). Su gate (vitest+typecheck+build) pasó VERDE: los tests nuevos
solo cubrían el caso nuevo, no el consumidor previo (panel de settings de org),
que quedó roto (422/403) sin que ningún test lo detectara.

Patrón: cuando delegas "añade X que use el endpoint Y", el subagente tiende a
re-propósito Y en vez de crear uno nuevo. Fix:
- Instruir: NO modificar endpoints existentes; crear uno nuevo si la audiencia/auth difiere.
- Tras el subagente: `grep -r "<endpoint>"` los consumidores y probar el flujo viejo.
- "Todo verde" del subagente ≠ sin regresión de integración cross-feature.
