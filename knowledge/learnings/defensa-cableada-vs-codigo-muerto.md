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

**Ampliación 2026-07-25 (auditoría de los 9 módulos IA: 13 placebos más).** Dos variantes que el grep NO caza:
- **Duplicado divergente**: el toggle duplica un campo cuyo owner real es otra tabla. El grep da cientos de hits (el owner sí la usa) y parece cableado. Caso: `regimen_iva`/`periodicidad_iva`/`estimacion_irpf` en el schema del módulo fiscal cuando el owner es la tabla `perfil_fiscal` → el usuario cambia el régimen y el 303 se sigue calculando con el viejo. Detección: por cada campo, "¿tiene otro owner?". Si sí, no va al schema: va un enlace al owner.
- **Espejo que se rellena solo**: borrar el campo del catálogo no basta si tu propio backend lo reescribe. Aquí `/api/fiscal/perfil` replantaba las 3 claves en el jsonb en cada guardado del wizard.
- El grep además necesita **quitar comentarios** antes de buscar (la única aparición de `guardar_historial` era un comentario) y limitarse a `src/` (una migración homónima da falso positivo).
Automatizable como red de seguridad, no como garantía. Lo que cierra el agujero de raíz: forzar `implemented:false` a todo campo que solo exista en BD — si no está en el catálogo, no puede tener consumidor en código. Ver [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]].
