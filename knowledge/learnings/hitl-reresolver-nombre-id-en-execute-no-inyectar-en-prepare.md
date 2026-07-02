---
title: en HITL, re-resuelve nombre→id en execute; no lo inyectes en prepare (el flujo de corrección lo salta)
date: 2026-07-02
source: claude-code-session
tags: [agentic, hitl, agh-iberica, diseño]
---

Bucle HITL propose→confirm→execute con `prepare` que resuelve un nombre hablado
→ id de una fila ("la oportunidad de Dragados" → opportunityId). Tentador: resolver
en `prepare` e inyectar el id en el write pendiente (como haces con valores puros:
`fireAt`, `occurredAt`). NO para lookups a store.

Motivo: el move de **corrección** del brain mergea los `fields` corregidos y re-propone
SIN volver a llamar a `prepare`. Si inyectaste el id y el usuario corrige el nombre
("no, era Endesa"), el write conserva el id viejo → escribe sobre la entidad equivocada,
justo lo que HITL debe impedir. Re-resolver en `execute` (lee el nombre corregido) se
auto-cura. Regla: inyecta valores derivados/puros; re-resuelve lookups a store.

Corolario: el bucle `confirm` ejecuta sin try/catch → un throw en `execute` estalla
POST-confirmación (mala UX). Pre-valida en `prepare` todo lo previsible (enum no
canónico, estado incompatible) y degrada a `clarify` ANTES de confirmar. Primo de
[[boton-hitl-referenciar-estado-persistido-no-id-efimero-proveedor]].
