---
title: FacturaIA — Conciliación bancaria + Copiloto v2 (spec definitiva)
date: 2026-05-19
source: docs/architecture/conciliacion-copiloto-spec.md (repo)
tags: [facturaia, conciliacion, copiloto, ia, psd2, gocardless, claude-sonnet-4-6]
---

# Conciliación bancaria + Copiloto v2 — Spec definitiva

**Estado**: arrancando 2026-05-19 · **Target deploy**: `app.tufacturaia.com`

Apuntador a la spec autoritativa en el repo: `docs/architecture/conciliacion-copiloto-spec.md` (2.075 líneas, 28 secciones).

Este subfile NO es la spec — es el resumen ejecutivo para Obsidian + entry-points. Cualquier divergencia entre este resumen y el documento del repo, el repo gana.

## Qué construimos

Dos features integradas que se potencian mutuamente:

1. **Conciliación bancaria** — módulo add-on 19€/mes. Cruza movimientos del banco con facturas. La IA propone matches con score + motivo. Auto-confirma los de alta coincidencia, revisa el resto.
2. **Copiloto v2 conversacional con tool-use** — drawer global (⌘K) con Claude Sonnet 4.6. Sabe en qué pantalla está el usuario, accede a datos de la org via tools tipados, ejecuta acciones (con confirmación humana obligatoria para destructivas). Incluido en plan Pro AI (NO add-on aparte).

## Por qué se hace ahora

- Diferenciador competitivo claro vs Holded/Quipu/Billin: explicabilidad de IA + Copiloto actuando sobre datos
- Reutiliza infra existente (movimientos_bancarios, triggers 061+101, módulo conciliacion en plan_features ya seedeado)
- Permite cerrar el loop "OCR factura recibida → conciliación automática → asistente que la explica"

## Plan en 2 sprints

### Sprint A — MVP (10-12 días laborables)

Validar adopción ANTES de invertir en PSD2/embeddings/Copiloto-full.

- **PR-A1** (5d) — Parser CSV/MT940/OFX + import + mig 105 (sugerencias, tablas Copiloto base, product_events). Última mig en repo verificada: 104. Mig 103 actual ya añadió `facturas.cobrada_con_movimiento_id` + dedup en triggers — mig 106 lo aprovecha, no lo reinventa.
- **PR-A2** (3d) — Trigger sugerencias deterministas + bandeja con 3 secciones colapsables (auto-conciliadas / pendientes / sin candidato) + RPC `confirmar_sugerencia`
- **PR-A3** (3d) — Copiloto v2 minimal con 4 tools core (getKPIs, searchFacturas, getDeudaPorCliente, composeCobroMessage) + streaming SSE + anti prompt-injection
- **PR-A4** (1-2d) — 50 casos golden Copiloto + evals CI + smoke E2E + telemetría 17 eventos producto + panel admin tabs (Conciliación + Copiloto)

### Sprint B — Expansión condicional (~25-30d)

Solo si métricas MVP cumplen: ≥30% activación, ≥50% precision, ≥40% Copiloto retention, ≥30% piden sync auto.

- **PR-B1** **TrueLayer Data API PSD2** (sync 6h + OAuth + consent watcher 90d + webhooks JWS). Pivot desde GoCardless BAD (cerró signups nuevos 2026-05-19). Cliente abstraído tras interfaz `Psd2Provider` para swap futuro a Tink/Afterbanks si tracción lo justifica.
- **PR-B2** Embeddings semánticos + pgvector HNSW + matching probabilístico
- **PR-B3** Copiloto memoria 3 niveles + tools adicionales según logs reales
- **PR-B4** IA invisible (duplicados + briefing diario + anomaly + predicción cobro)

## Decisiones clave (ver §Apéndice A en repo)

| ID | Decisión | Razón |
|---|---|---|
| D-001 | Dokploy cron, NO n8n, para crons del módulo | Código en monorepo + observabilidad unificada + precedente verifactu-process |
| D-002 | 3 tabs `Por revisar / Movimientos / Historial` (NO 2 tabs con IA suffix) | Auto / pendientes / sin-candidato son mental models distintos |
| D-003 | `% de coincidencia` (NO `confianza` ni `score`) | Más neutro, alineado con glosario contable |
| D-004 | Token CSS `--brand-text` separado de `--brand` | `#3D7BF5` no pasa WCAG AA 4.5:1 para texto pequeño |
| D-005 | Trigger SQL crea sugerencia con `auto_confirmed=true`, NO toca `facturas.estado` directo | RPC `confirmar_sugerencia` único path |
| D-006 | Sprint B condicional a métricas | Validación de mercado antes de 30d más de inversión |
| D-007 | Copiloto incluido en Pro AI, NO add-on aparte | Diferenciador comercial, no fragmentar |
| D-008 | Rol `support_l1/l2` separado de `OrgRole` | Soporte sin impersonar |
| D-009 | ESC cierra drawer pero NO aborta streaming Copiloto | Tokens parciales se persisten, evita perder coste OpenAI ya pagado |
| D-010 | 4 tools Copiloto Sprint A (NO 15) | Expansión según logs reales de uso |
| D-011 | Cron sync cada 6h (no 1h) | Regulatorio PSD2: max 4 retrievals/24h/account |
| D-014 | **TrueLayer Data API** (no GoCardless BAD) | GoCardless BAD cerró signups nuevos. TrueLayer self-service, free tier, FCA UK + CBI EU. Tink futuro si tracción |
| D-015 | Cliente PSD2 detrás de interfaz `Psd2Provider` | Swap proveedor futuro sin tocar schema/RLS/UI |

## Cómo se integra en la UI

- **Sidebar**: nuevo ítem "Conciliación" entre Cashflow e Informes (solo si feature activa, con badge de sugerencias pendientes)
- **Topbar**: botón ⌘K Copiloto en toda la app (drawer 480px lateral derecho, full-screen mobile)
- **Settings**: card add-on en `?tab=plan-billing`, modal config en `?tab=modulos → Conciliación`
- **Admin**: tabs nuevos en `/admin/system?tab=conciliacion` y `?tab=copiloto` con KPIs cross-org, observabilidad, soporte sin impersonar, frases-tipeadas para acciones destructivas

## Compliance crítico (ver §22 repo)

- **PSD2**: scope mínimo `transactions+balances`, NUNCA `payment_initiation`. Acuerdo max 90d. Cron expiry-watcher con avisos T-14d/T-7d/T-1d.
- **GDPR**: DPA firmado con OpenAI + Anthropic + GoCardless ANTES de Sprint B. Botón opt-out IA en admin. Cascade delete al desactivar org.
- **AEAT inviolable**: ningún tool del Copiloto puede mutar `facturas.concepto|total|num|lineas`. CI guard verifica.

## Anti-features (ver §28 repo)

20 cosas que NUNCA hacer. Las 5 más críticas:

1. NO `aria-pressed` para selección exclusiva — `role="radiogroup"` siempre
2. NO `var(--brand)` como color de texto — usar `var(--brand-text)`
3. NO mezclar auto-conciliadas con pendientes en lista plana
4. NO `org_id` desde body/LLM — siempre server-side desde sesión
5. NO mutar `facturas.concepto|total|num` desde tools Copiloto — CI guard

## Pre-requisitos a verificar (antes de cada PR)

- [ ] `claude-sonnet-4-6` ID exacto disponible en cuenta Anthropic
- [ ] Prompt caching Anthropic activable
- [ ] Pool mode Supabase (transaction vs session) para advisory locks
- [ ] Next 16 SSE en App Router — leer `node_modules/next/dist/docs/`
- [ ] DPA OpenAI + Anthropic + TrueLayer firmados (Sprint B antes de mig 107)
- [ ] TrueLayer free tier exacto (connections/mes) — verificar al signup `console.truelayer.com`
- [ ] TrueLayer lista bancos España — verificar `GET /api/providers?country=es` con client_id real
- [ ] TrueLayer approval producción (sandbox inmediato, prod ~5d review)

## Specs relacionadas

- [[facturaia-open-banking-psd2]] — spec legado de PSD2 (cubierto y ampliado por este)
- [[facturaia-bloque-4-agent-query-spec]] — copiloto IA multi-canal (precursor del Copiloto v2)
- [[facturaia-comunicaciones-emails]] — outbox + plantillas (reutilizable para notif PSD2 expiry, briefing diario, etc.)
- [[facturaia-integracion-api-v1-portal]] — convenciones API que aplican a `/api/internal/conciliacion/*`

## Histórico de cambios de esta spec

- **2026-05-19** — Creación. Sintetizada de 11 agentes especialistas (seguridad, BD, frontend, IA, arquitectura crítica, estrategia entrega, IA-design, IA-arquitectura, microcopy, a11y, admin). Versionada en repo bajo `docs/architecture/`.
