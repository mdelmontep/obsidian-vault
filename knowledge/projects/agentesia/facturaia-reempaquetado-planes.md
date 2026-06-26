---
title: FacturaIA — Reempaquetado de planes (tier Plus + escalonado + soft-limits)
date: 2026-06-26
source: Auditoría de pagos + estrategia pricing (sesión Claude 2026-06-26)
tags: [facturaia, pricing, planes, billing, stripe, producto]
---

# Reempaquetado de planes FacturaIA

Estrategia de pricing aprobada por Manu (2026-06-26) tras auditoría de pagos. La **Fase 1** (bugs + conexión + soft-limits) ya está en PR #509. La **Fase 2/3** (tier Plus + reempaquetado + grandfathering) está pendiente de crear prices en Stripe live.

## Estrategia aprobada (decisiones)

- **1B — Trial sin tarjeta**: ya existe de facto (trigger `130`: 14 días en `billing_status='trial'` sin pasar por Stripe). Solo el checkout de conversión pide tarjeta. Ajuste opcional 1-2 líneas en `base-checkout.ts:234-236` si se quiere que la conversión no arrastre `trial_period_days`.
- **2B — Soft-limits** (no muro 429): aviso al 80% + bloqueo suave con CTA upgrade en cuotas baratas (facturas, OCR); overage facturado solo donde el coste marginal es real (WhatsApp/IA — ya existe en cobros). Parcialmente hecho en Fase 1 (copiloto + OCR → modal con CTA).
- **3 B+C-lite — Tier intermedio + ancla**: nuevo **Plus 29€** entre Starter (14€) y Profesional (49€). Enterprise se queda en **99€** visible.
- **4 — Value metric doble**: facturas para el tier base + IA/WhatsApp por consumo (cuotas separadas ya existen).
- **5 — Add-ons híbrido**: fiscal sigue como add-on (único con checkout Stripe real); conciliación, antifraud y stock se pliegan en tiers (dejan de ser add-ons).

## Matriz de tiers propuesta

| Bloque | Starter 14€ | Plus 29€ | Profesional 49€ | Enterprise 99€ |
|---|---|---|---|---|
| Facturación core | ✓ | ✓ | ✓ | ✓ |
| Plantillas factura | 1 | 4 | 4 + custom | + editor bloques |
| OCR | básico | medio | alto | ilimitado |
| Copiloto IA | — | solo lectura | + acciones (crear/editar) | + ilimitado |
| WhatsApp/voz | factura+presupuesto | + cuota media | + proforma+abono | ilimitado |
| Cobros | — | básico (~150) | 500 + overage | 2.000 + overage |
| Conciliación | — | — | **asistida** (importar+match+marcar+anticipos) | **inteligente** (IA enrich + banco directo PSD2) |
| Cashflow | — | básico | + previsión IA (fiscal+RETA) | + horizonte extendido |
| Stock | — | — | ventas (descuento, PMP) | + compras + FIFO (roadmap) |
| Multiempresa | 1 | 1 | 2 | 5+ |
| SEPA | — | — | remesas cobro | + remesas pago |
| Antifraude | — | — | — | facturas + banco |
| Fiscal (303/130) | Add-on 14,90€ | Add-on | Add-on | Add-on |

Cuotas sugeridas Plus: facturas 150, OCR 100, WhatsApp msgs 800, copiloto 1,5M tokens, cobros 150 envíos, 1 empresa.

## Decisiones de escalonado clave

- **Conciliación se parte** (ya separada por archivos): base (`conciliacion`: import + match + marcar + anticipos) en Pro; IA (`ai-enrich.ts`) + banco directo PSD2 (`psd2/`, `banks/*`) en Enterprise. Requiere 2 sub-flags nuevos: `conciliacion_ia` y cablear `integracion_banco` (la feature YA existe en BD mig 004 pero NUNCA se consulta; las rutas `banks/*` solo tienen gate de rol, no de feature).
- **Stock**: ventas y compras+PMP YA implementados (copy "compras próximamente" del catálogo está desactualizada). FIFO no existe (solo PMP). Stock-ventas a Pro.
- **Copiloto**: read en Plus, write en Pro vía toggle `permitir_acciones` (hoy `implemented:false`, hay que construirlo).

## Fase 2 — implementación (pendiente)

1. **Migración**: `INSERT plans('plus', 29, anual 278.40, orden 2, ...)` + renumerar `orden` de pro(3)/enterprise(4); seed `plan_features`+`plan_limits` para `plus`; crear feature `conciliacion_ia`; reasignar features según matriz.
2. **~9 literales TS/Zod** acoplados a 3 planes: `PlanId` union y `PLAN_ORDER` en `stripe-plans.ts`; `z.enum` en `checkout-plan`/`change-plan`/`admin/cobros/quotas`; `.includes` en `stripe-webhook:281`; `PlanId`/`PLAN_ORDER`/`PLAN_HIGHLIGHTS` en `plan-billing.tsx`; `planIncluido` en `catalog.ts`/`modulos-section.tsx`; `PLAN_RANK` en `agentes-view.tsx`. La UI de pricing lee planes de BD → la 4ª columna aparece sola (revisar CSS `pb-plan-grid` para 4 cols).
3. **Sub-flags gating**: `conciliacion_ia` (enrich-batch, sugerencias, reglas-aprendidas) e `integracion_banco` (`banks/*` vía `requireFeature` de `withApiAuth`).
4. **Grandfathering**: snapshot a `org_features` (source apropiado) de TODO lo que las orgs actuales (active + trial, excluir complimentary/internas) tienen HOY, ANTES de cambiar `plan_features`. Crítico: el reempaquetado mueve copiloto/whatsapp fuera de Starter y parte conciliación; sin snapshot, clientes pierden acceso.
5. **Sidebar descubribilidad** (decisión UX): hoy oculta features no incluidas; recomendado mostrar con candado + CTA para conversión.

## Fase 3 — activar (requiere acción de Manu)

- Crear 2 prices en **Stripe LIVE**: Plus mensual 29€ y anual 278,40€ (interval month/year, `tax_behavior=exclusive`).
- Setear `STRIPE_PRICE_ID_PLUS_MENSUAL` y `STRIPE_PRICE_ID_PLUS_ANUAL` en Dokploy (recrear container, no restart). El código degrada a 503 hasta entonces.
- Push de la migración de reempaquetado a prod tras verificar el grandfathering con datos reales.

## Incoherencias detectadas a limpiar en Fase 2

- `pro.conciliacion` tiene `enabled=true` Y `addon_purchasable=true` (19€) simultáneamente.
- `plans.starter.precio_mes=14` en prod pero mig `204` decía 19 (editado por panel; reconciliar canónico).
- `stock` en `disponibilidad='beta'` = add-on de pago accesible gratis para todos (fuga de ingresos). Cerrar al reempaquetar.
- `admin_dashboard_stats` MRR suma solo `precio_mes`, ignora anual y add-ons.

Ver auditoría de conexión en PR #509. Hub: [[facturaia]].
