---
title: "n8n: webhook authentication:none + toolCode con SERVICE_ROLE_KEY = acceso privilegiado sin auth, vivo aunque el workflow no reciba tráfico"
date: 2026-07-05
source: claude-code-session
tags: [n8n, seguridad, service-role, decomision]
---

Un nodo Webhook n8n con `authentication:none` expone una URL pública (`/webhook/<path>`). Si nodos aguas abajo (langchain agent + toolCode) leen `$env.SUPABASE_SERVICE_ROLE_KEY` y pegan a la BD sin gating, cualquiera que POStee un payload con la forma esperada obtiene **escritura privilegiada** — y sigue vivo aunque el workflow tenga 0 ejecuciones legítimas (p.ej. tras un cutover de webhook a otro sistema). Que esté "fuera del camino" ≠ cerrado.

Fix / decomisión:
- `POST /api/v1/workflows/{id}/deactivate` cierra el webhook al instante (responde 404 not-registered). Reversible, sin borrar nada.
- Luego borrar los nodos peligrosos por API (`PUT` con el JSON sin ellos; `settings` solo con keys que acepte el schema, p.ej. `executionOrder` — quitar `binaryMode`).

Antes de ejecutar un plan de decomisión escrito en otra sesión: **re-auditar el flujo real** (¿quién llama a quién hoy?). El plan asumía "montar relay de texto"; el receptor estaba 100% out-of-path (Meta→Next.js, sin reenviar a n8n) → desactivar+limpiar, no relay a la nada. Ver [[facturaia-g5a-005-plan-decomision-n8n]].
