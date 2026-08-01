---
title: un helper de auditoría con early-return silencioso deja sin traza justo las acciones globales
date: 2026-08-01
source: claude-code-session
tags: [auditoria, observabilidad, admin, anti-patron]
---
`logAdminAction(userId, accion, orgId, …)` empieza con `if (!orgId) return`. Las acciones por-org
pasan un `orgId` y se registran; las GLOBALES (precios de plan, `plan_features`, catálogo de
features, disponibilidad de módulos, invitaciones) llaman con `null` y **no escriben nada**. El
código lee como si auditara, así que nadie lo revisa: 11 escrituras, cero filas, desde siempre.

Lo grave es el sesgo: lo que se pierde es exactamente lo de mayor radio (lo que afecta a TODOS los
clientes), y queda auditado lo pequeño. Con varios superadmins, un cambio de precio es
irreconstruible.

Cómo se detecta sin leer código, que es lo que lo hace útil: contar por patrón de acción sobre el
histórico. `accion ilike *feature*` → 542 filas, TODAS con `org_id`; `*price*`, `*plan*`, `*modulo*`,
`*invite*` → 0. El contraste ES la prueba.

Regla: un helper de traza no hace early-return silencioso. O acepta el caso sin org (sink global,
tipo `admin_audit_log`) o lanza. Y al auditar observabilidad, medir la DISTRIBUCIÓN de acciones
registradas, no comprobar que la tabla tiene filas.

Ver [[auditoria-que-es-la-unica-copia-del-dato-no-puede-ir-en-fire-and-forget]]
