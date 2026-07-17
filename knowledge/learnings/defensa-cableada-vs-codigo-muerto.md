---
title: una defensa de seguridad sin consumidores = código muerto = falsa seguridad
date: 2026-06-17
source: claude-code-session facturaia
tags: [seguridad, auditoria, billing]
---

Que exista una función de control de acceso NO significa que esté activa. Hay que grepear sus **consumidores**, no solo su definición.

Caso real (pentest TuFacturaIA): `requireWriteAccess(orgId)` en `src/lib/billing.ts` comprobaba `billing_status ∈ {expired,suspended,cancelled}` y devolvía 403 — pero **ningún endpoint la llamaba** (grep: 1 sola ocurrencia, su `export`). Resultado: orgs morosas/suspendidas seguían facturando por web y por API v1. "Suspender" no hacía nada → bypass de pago silencioso.

Fix: cablear el gate en el pipeline central (`withApiAuth` + `withApiV1`), no en cada endpoint (se olvida uno). Mismo patrón que el kill-switch read-only que ya vivía al lado.

Variante (config/feature toggles): un campo de `config_schema` marcado `implemented:true` sin consumidor = toggle decorativo que miente al usuario. Caso TuFacturaIA módulo OCR (PR #990): `auto_categorizar` (implemented:true) no lo leía nadie → guardaba en BD pero la categoría se aplicaba SIEMPRE. Fix: gatear la escritura + test ON/OFF. Auditar config es igual: por cada toggle que promete comportamiento, grep su consumidor.

Regla de auditoría: por cada helper de seguridad (`require*`, `assert*`, `check*`, guards) O flag/toggle de feature, `grep` sus llamadas/lecturas. 0 consumidores = agujero o feature falsa + falsa sensación de cobertura. Relacionado: [[postgres-revoke-public-no-elimina-grants-individuales]].
