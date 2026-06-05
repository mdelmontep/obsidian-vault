---
title: multiempresa saas: navegar=membresía, agregar=propiedad, cobrar=cuenta (no mezclar)
date: 2026-06-05
source: claude-code-session
tags: [saas, multi-tenant, rgpd, arquitectura]
---
En un SaaS donde un usuario opera varias entidades hay 3 ejes que parecen "lo
mismo" pero NO lo son; mezclarlos da bugs y riesgo legal:
- Navegar/cambiar (selector, bot WhatsApp) → por MEMBRESÍA (todo a lo que accedes).
- Agregar/comparar/sumar (métricas, dashboards, copiloto) → por PROPIEDAD (rol
  owner/admin): solo TUS entidades. Agregar por membresía cruda suma datos de
  clientes que solo gestionas → consolida responsables RGPD distintos
  (desviación de finalidad) + cifras engañosas.
- Cobrar/cuota/límite de plan → por CUENTA de facturación (subscription).
Caso TuFacturaIA: el módulo multiempresa mezcló los 3 → mostraba "1 empresa" a
quien tiene 2 y, en membresía, filtraba datos de clientes. Fix: cada feature
elige su eje explícito (`.in('rol',['propietario','admin'])` para agregar).
Ver [[rls-multi-org-active-vs-membership]] · [[ADR-028-multiempresa-scope-navegar-agregar-cobrar]].
