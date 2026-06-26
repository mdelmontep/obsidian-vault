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

Regla: al auditar enforcement, enumerar TODOS los puntos de entrada (web + v1 +
voz/WA + cron + MCP) y verificar cada uno. Mejor aún: centralizar el gate en la
fuente única de la acción (createDocument, helper de ingesta) en vez de en cada
wrapper, o gatear en el wrapper de cada canal. Ver [[endpoint-toggle-feature-debe-gatear-enable-por-plan-o-compra]].
