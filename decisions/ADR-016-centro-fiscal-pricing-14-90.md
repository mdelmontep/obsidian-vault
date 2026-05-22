---
title: ADR-016 — Centro Fiscal IA pricing 14,90€/mes (149€/año), no 9€ spec original
date: 2026-05-22
status: accepted
tags: [adr, facturaia, fiscal, pricing, gtm]
---

## Contexto
Spec original proponía 9€/mes add-on Pro. Sin validar con mercado. Stripe checkout aún no conectado en producto (toggle add-ons sin cobro real).

## Opciones consideradas
- **A — 9€** spec original: percibido commodity Netflix-tier, recupera dev solo con 6.500 orgs activas. Riesgo "barato = no fiable" para herramienta fiscal.
- **B — 14,90€ (149€/año -17%)**: mediana exacta del mercado SaaS contable ES 2026 (Anfix 14,99 / Holded Basic 14,50 / Quipu Starter 14 promo). Recupera dev con 1.200 orgs.
- **C — 19€**: territorio Quipu Pro/Holded Pro. Entra cuando ya tienes presentación telemática (v3+). Sin esa promesa → drop conversión.

## Decisión
**B**. 14,90€/mes con descuento anual -17% (149€/año). Trial 14 días sin export TXT/XLSX (anti-canibalización de pago por trimestre).

## Consecuencias
Validado vs research mercado online 42 fuentes (Trustpilot/Capterra/Reddit/Foros). Pricing alineado con paridad de feature ("no presenta" como mercado). Justifica desarrollo MVP 4 sem + auditoría externa pre-beta 10-15k€. Si validación post-beta muestra <40% conversión a 14,90€, bajar a 12,90€ antes que cambiar scope. Bundle "Cierre" (Conciliación 19€ + Fiscal 14,90€ = 24,90€) deferred a v1.5 — primero validar fiscal solo.
