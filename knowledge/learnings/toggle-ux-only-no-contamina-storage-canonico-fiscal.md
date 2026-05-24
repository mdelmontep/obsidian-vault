---
title: toggle UX-only (precio inclusive, fechas, divisas) NO contamina storage canónico
date: 2026-05-24
source: claude-code-session
tags: [architecture, fiscal, storage-canonical, ux-toggle]
---

Para "modos de entrada" UX (precios con IVA incluido, fechas en otro formato, divisas alternativas, etc), tentación inicial: añadir columna `precio_modo: 'bruto'|'neto'` por row. **Mala idea** en apps fiscales/financieras.

**Patrón correcto**:
- Storage SIEMPRE en formato canónico (base imponible neta, ISO date, EUR x100). Una fuente de verdad.
- Toggle persistido como UX preference de la org (`organizations.default_precio_iva_incluido`) — default visual del input.
- Sesión por documento en `sessionStorage[doc_id]` — override puntual sin tocar BD.
- Conversión solo en pipeline render input ↔ storage. Tests cubren el sandwich.

Razones: Verifactu/AEAT 303/libro IVA leen base. Si guardas "total inclusive" hay que recalcular base con redondeo cada lectura → drift acumulado, hash inestable, divergencia entre reportador SQL y endpoint. La columna `precio_modo` además duplica fuentes de verdad en 4 RPCs + calculador 303 (cada sitio ramifica).

Aplica a cualquier "input ≠ storage" en apps fiscales. Caso real FacturaIA mig 161 + sprint formulario 2026-05-24. Ver [[ADR-019-precio-inclusive-iva-storage-canonico-vs-columna-precio-modo]].