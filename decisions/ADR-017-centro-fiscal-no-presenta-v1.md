---
title: ADR-017 — Centro Fiscal IA v1 NO presenta telemáticamente, convenio AEAT diferido
date: 2026-05-22
status: accepted
tags: [adr, facturaia, fiscal, legal, aeat]
---

## Contexto
Presentar telemáticamente modelos AEAT exige una de 3 vías: (a) cliente firma con cert/Cl@ve PIN, (b) SII (solo grandes >6M€), (c) convenio Colaborador Social RD 1065/2007 (TuFacturaIA presenta con SU cert empresa previo apoderamiento del cliente). Pure-play SaaS contable ES (Quipu/Holded/Anfix/Contasimple) no presentan; Declarando sí porque tiene asesores humanos en plantilla.

## Opciones consideradas
- **A — Presentar v1 vía Colaborador Social**: requiere convenio AEAT 3-6 meses + RC obligatorio (~1.500-3.000€/año) + responsabilidad solidaria art 92 LGT (sanción cae sobre cliente Y TuFacturaIA) + apoderamiento individual de cada cliente (UX cuello de botella). Sin clientes pagando todavía.
- **B — Modelo Declarando**: gestoría online con asesores humanos en plantilla. Modelo de negocio distinto (asesoría + software), no SaaS puro escalable.
- **C — NO presentar v1, diferir convenio a 50 clientes pagando**: paridad con Quipu/Holded/Anfix. Marketing honesto "te genero el fichero y te guío clic a clic en sede AEAT". Arrancar gestión convenio cuando haya base validada.

## Decisión
**C**. v1 entrega TXT BOE-ready + PDF + libro IVA XLSX + share asesor. Cliente sube él al portal AEAT con Cl@ve PIN. v3 (mes 8-12 post-MVP) presentará vía colaborador social SI hay 50+ clientes activos.

## Consecuencias
Research mercado online confirma "no presenta" NO mata venta (5+ frases verbatim asesores y autónomos). Reduce riesgo legal MVP (sin responsabilidad solidaria) y coste fijo (sin RC obligatorio hasta v3). Cuando v3: arrancar `comercial.ceres@fnmt.es` + alta CNAE compatible + Hiscox/AXA + apoderamientos masivos con onboarding guiado. Sello eIDAS FNMT TS@ + WORM Backblaze ya implementados en MVP cubren probatoriedad inmutabilidad (RD 1619/2012 art 8.1) aunque no presentemos.
