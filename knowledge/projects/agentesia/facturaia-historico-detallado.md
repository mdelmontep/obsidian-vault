---
title: facturaia — histórico detallado
date: 2026-05-31
tags: [cliente, facturaia, historico]
---

Índice del histórico de FacturaIA. El contenido pesado vive partido en los ficheros de abajo (uno por snapshot de poda del hub, más uno de eventos puntuales con fecha propia). El hub vivo y actual es [[facturaia]].

- [[facturaia-historico-snapshot-2026-05-31]] — snapshot fundacional del hub (contenido original del archivo desde su creación): log cronológico en blockquotes (~2026-05-16 a 2026-07-19), foto congelada del hub a 2026-05-31 (Estado actual, NOW, Smoke, WIP, Progreso en vivo, NEXT, LATER, Decisiones, Bloqueos, Seguridad, Stack, credenciales, histórico de hitos) y la Auditoría SaaS 2026-05-29.
- [[facturaia-historico-snapshot-2026-06-15]] — dos podas del hub del mismo día: "dieta del hub" (Estado/NOW/PRIORIDADES/Progreso en vivo/Decisiones/Histórico de hitos) y "purga hub" (NEXT/Smoke/Bloqueos/WIP cerrados movidos).
- [[facturaia-historico-eventos]] — entradas de evento puntual con fecha propia en el header, 2026-06-16 a 2026-07-13 (informes de analítica, bug NIF proveedor, stock por lotes, hitos 06-28→07-04, dedup NOTES, ingesta, drawers, cierre de pendientes).
- [[facturaia-historico-snapshot-2026-07-15]] — poda del NOW del hub a 2026-07-15.
- [[facturaia-historico-snapshot-2026-07-23]] — poda más reciente del hub a 2026-07-23 (Obras: certificación/ficha/adicionales/retención de garantía, modales adaptables, nombres por UUID).
- [[facturaia-historico-snapshot-2026-07-25]] — poda del NOW del hub a 2026-07-25: 38 entradas cerradas (Obras completo, unificación UI, Centro Fiscal, billing/cupones, Slack, seguridad npm, ticket-runner, import de extractos, API v1 Obras).
- [[facturaia-historico-snapshot-2026-07-27]] — poda del 27-jul: 12 entradas cerradas del NOW (gate del 26-jul y sus remates, vigilante externo, lote conciliación, retención del copiloto, Obras, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta).
- [[facturaia-historico-snapshot-2026-07-28]] — poda del 28-jul: 10 entradas cerradas del NOW (IVA negativo de presupuestos, `/api/health` con versión real, ticket de vencimiento de IET, panel `/admin` sin falsas incidencias de precios + `proxy.ts`, gate del 26-jul y sus remates, lote de conciliación).
- [[facturaia-historico-snapshot-2026-07-29]] — dos podas del 29-jul: la de la mañana y, al cierre, 11 entradas más del NOW (área de tickets y su fuga de mensajes internos, avisos de respuesta del cliente, impersonación en listados, VeriFactu, coste LLM, prompt caching, auditoría Fable 5, cola OCR, UX de ingesta, recurrentes).
- [[facturaia-historico-snapshot-2026-07-30]] — poda del 30-jul: los 4 smokes de prod que Manu ya verificó (runner, OCR de nº de factura y RAEE, condiciones de pago en PDF, impersonación tras `proxy.ts`).

## Módulo Obras — entrada retirada de `top-of-mind` el 03-ago-2026

**Módulo Obras (mini-ERP instalaciones, sustituye WAPI) EN PRODUCCIÓN.** Núcleo + FASE 2 + **FASE 3 (PR #999, 18-jul)** mergeados a main y con smoke prod verde. FASE 3 = decisiones de Natalia: coste MO fiel (tarifa por instalador, precio hora especial por obra, dieta default, calendario mensual de partes), módulo **Herramientas** (foto+event log+alta por WhatsApp vía copiloto), corregir descuento/precio desde recibida, **proforma a origen** (informe PDF, NO createDocument, ADR-obras-001), generar pedido desde presupuesto con expansión de UO, chip recibido X/Y. Migs 471-511 reconciliadas (schema_migrations local==remote). `/fia-cierre` cross-issue cazó 2 bloqueantes que los gates por-issue no vieron (`.or()` sin entrecomillar en tools copiloto con test mock no-op → ver [[postgrest-or-no-escapa-delimitadores]]; clave React/dedup rota al componer olas). **Org REAL de Natalia**: "Instalaciones Eléctricas y de Telecomunicación, S.A." (`b9d5d6f7-…`, is_test=false, creada 16-jul, miembro `administracion@iet.es`). Sembrado el catálogo de **745 tipos M.O.** (copiado del Sandbox, suma horas 3826,901 idéntica, 18-jul). Docs `docs/architecture/obras/fase3-plan-decisiones.md` + ADRs 001/002/003.
