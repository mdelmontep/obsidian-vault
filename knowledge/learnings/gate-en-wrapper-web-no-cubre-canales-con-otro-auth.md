---
title: un gate que vive solo en el wrapper web no cubre los canales con otro auth
date: 2026-06-26
source: claude-code-session
tags: [auth, multi-tenant, billing, cuotas, auditoria]
---

El gate de plan/billing/cuota suele vivir en el wrapper de sesión (`withApiAuth`).
Pero el negocio entra por MÁS puertas: API pública (`/api/v1/*`, `withApiV1`),
voz/WhatsApp (`requireServiceAuth`, n8n), crons (`/api/internal/*`), conector MCP.
Esas NO pasan por el wrapper web → el gate no se aplica.

Caso real FacturaIA: el gate read-only (cuenta morosa) solo estaba en `withApiAuth`
→ una org suspendida seguía facturando y gastando IA por el bot. Y `whatsapp_msgs`
solo se enforce-aba en la web. El conector MCP (v1 user-token) no gateaba feature.

**Estado 2026-07-27** — un mes después este learning seguía sin accionar. Medido:
de 90 rutas `/api/internal/*`, solo 13 gateaban, copiando el código a mano (una de
ellas con el comentario "el gate read-only de withApiAuth NO cubre estos endpoints",
replicado 5 veces y olvidado en 82). Extraído `orgWriteGate()` a
`lib/auth/core/write-gate.ts` y cableado en `requireServiceAuth`, pero **en log-only**
hasta `INTERNAL_WRITE_GATE_ENFORCE=true`: encender el bloqueo de golpe en 82 crons
puede dejar el sistema sin camino de recuperación (un cron de cierre de cuenta
bloqueado por el propio kill-switch). Denegaciones a `admin_audit_log`
(`internal.write_gate_would_block`) para decidir con datos. Exenciones explícitas:
recuperación, retención, purgas. Ver [[helper-de-auth-que-asume-validacion-del-caller]].

Lección de proceso: un learning escrito y no accionado no protege de nada. Si el
hallazgo es de enforcement, además de aquí va a `top-of-mind` con dueño.

Regla: al auditar enforcement, enumerar TODOS los puntos de entrada (web + v1 +
voz/WA + cron + MCP) y verificar cada uno. Mejor aún: centralizar el gate en la
fuente única de la acción (createDocument, helper de ingesta) en vez de en cada
wrapper, o gatear en el wrapper de cada canal. Ver [[endpoint-toggle-feature-debe-gatear-enable-por-plan-o-compra]].
