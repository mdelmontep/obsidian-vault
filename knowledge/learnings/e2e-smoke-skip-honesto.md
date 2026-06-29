---
title: E2E smoke — skip honesto por precondición, no falso rojo
date: 2026-06-27
source: TuFacturaIA PR #531
tags: [e2e, playwright, testing, facturaia, feature-gating]
---

Un smoke que da 20 rojos falsos tapa el rojo nº 21 que sí importa. Cuando un spec
depende de una **precondición** (módulo activo, rol superadmin, dato sembrado,
env), debe **skipear con razón**, no fallar.

- **Fuente autoritativa para gating**, no señal frágil: helper
  `featureActive(request, slug)` lee `GET /api/settings/features` (el mismo
  endpoint del panel de módulos). NUNCA detectar por texto de UI/EmptyState
  (cambia) ni por un 404 de endpoint (confunde "módulo apagado" con "endpoint
  roto" = la regresión que quieres ver).
- **Regla inviolable**: el skip es SOLO por precondición ausente. Si la
  precondición se cumple, el test corre entero. Jamás relajar/`.first()`-ear una
  aserción que cazaría un bug real (ej. fiscal-perfil que renderiza siempre → si
  falla es regresión, déjalo rojo).
- **No silenciar caps**: el probe de seed pagina → pide `?limit=500`, o un seed
  presente-pero-fuera-de-página-1 daría over-skip silencioso.
- Slug `plantilla_custom` NO está en `MODULES_CATALOG` → no sale en el endpoint;
  para esos casos usar la señal de bloqueo real en UI (`.tpl-gallery-lock`).

Patrón: `test.beforeEach(async ({ request }) => test.skip(!(await featureActive(request,'conciliacion')), 'módulo no activo (precondición, no regresión)'))`.

- **API endpoint como precondición**: si el smoke llama a una API (render-pdf, signed URL…) y devuelve 404 porque el dato de prueba no existe en sandbox (PDF no generado, recurso no sembrado), eso es precondición ausente, no código roto. Probar N hrefs en un loop, skip si ninguno devuelve 302; no fallar al primer 404.

Ver también [[smoke-test-mode-contamina-bd-prod-si-la-fn-escribe-bd]].
