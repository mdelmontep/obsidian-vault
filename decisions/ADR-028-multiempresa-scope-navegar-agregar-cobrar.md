---
title: ADR-028 — Multiempresa: navegar=membresía, agregar=propiedad, cobrar=cuenta
date: 2026-06-05
status: accepted
tags: [adr, facturaia]
---

## Contexto
El módulo Multi-empresa mostraba "1 empresa" a usuarios que gestionan 2. El schema ya separa `organizations` (empresa/workspace) de `billing_accounts` (suscripción) de `org_members` (acceso), pero el módulo (métricas, copiloto, selector) no tenía claro qué eje usar. Realidad: 6 orgs, cada una su propia `billing_account` (backfill 1:1 mig 215), 5 usuarios miembros de 2 orgs en cuentas distintas. Sin clientes de pago aún.

## Opciones consideradas
- **A. Por cuenta (`billing_account`)** — fiel al pricing "una suscripción, N empresas", pero regresa a "1 empresa" (cada org legacy = su cuenta). No resuelve la queja.
- **B. Por membresía cruda (`org_members`)** — muestra todas tus orgs, pero agrega datos de clientes que solo gestionas → riesgo RGPD (consolida responsables distintos) y cifras engañosas.
- **C. Por propiedad (rol propietario/admin) + 3 ejes separados** — tus negocios para agregar; membresía para navegar; cuenta para cobrar.

## Decisión
**C.** Tres ejes que no se mezclan: **navegar** (selector, empresa por defecto, WhatsApp) → membresía; **agregar/comparar** (métricas, copiloto `compararEmpresas`) → propiedad (`rol IN propietario/admin`); **cobrar** (incluidas/+12€/cuota) → `billing_account`. Validado con análisis de 4 agentes (arquitectura/pricing/UX/fiscal). PRs #155/#156.

## Consecuencias
Orgs de clientes que solo gestionas (gestor/contable) NO se agregan (correcto RGPD/fiscal). Pricing intacto ("1 incluida +12€/extra", diferenciador vs Holded/Xero). NO se consolidan los legacy (cada org su cuenta; consolidar caso a caso vía runbook futuro cuando un cliente pida factura conjunta). Pendiente futuro: panel asesor ("empresas que gestiono", listar sin agregar) + guard `is_account_owner` para billing. Regla transferible en [[multiempresa-saas-tres-ejes-navegar-agregar-cobrar]].

## Actualización 2026-06-05 (PR #157, audit cross-PR)
Corolario de pricing del eje "agregar=propiedad": la feature `multiempresa` se **alineó con la cuota** → incluida en **Pro** (mig 230), no enterprise-only. Motivo: Pro ya tiene cuota de 2 empresas y recibía **403** al intentar consolidarlas. Frontera: cuota > 1 empresa → tiene el módulo; Enterprise se diferencia por volumen (5). Source of truth del eje propiedad extraído a helper `getOwnedOrgs`/`getOwnedOrgIds` (`src/lib/auth/owned-orgs.ts`). Smoke E2E Pro verde. Regla de pricing en [[feature-atada-a-capacidad-del-plan-no-se-cobra-aparte]].
