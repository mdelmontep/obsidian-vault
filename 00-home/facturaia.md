---
title: facturaia
date: 2026-05-07
tags: [cliente, facturaia]
---

# FacturaIA

App SaaS de facturación con IA (OCR, agente WhatsApp, voz, recomendador). Multi-tenant.

## Estado

- **Producción**: facturaia.agentesia.world (Dokploy)
- **Stack**: Next 16 + Supabase + n8n + OpenAI Vision + Anthropic
- **Plan**: Starter / Pro / Enterprise + add-ons individuales (Conciliación 19€, Anti-fraude 9€)
- **Orgs activas**: AgentesiaLab (Enterprise), tecnocloud (Enterprise), Borja Galván (Enterprise), AgenteIA PRUEBA (Starter)

## Próximos hitos

1. **Pestaña notificaciones por org** (NOW) — campana topbar + drawer feed
2. **Tests proformas + abonos rectificativos** (NOW)
3. **Stripe en activación add-ons** (NEXT) — convertir toggle en compra real
4. **Cobros backend** (NEXT) — recordatorios escalados, alta conversión

## Bloqueos / esperando a terceros

- Dani+Gonzalo: subir certificado P12 + Declaración Responsable AEAT (SIF)
- Borja: review/merge agency-portal PR #54 y #55

## Links rápidos

- [Github](https://github.com/AgentesIA-MAdrid/facturaia)
- [Dokploy](https://dokploy.agentesia.world)
- [App](https://facturaia.agentesia.world)
- [Manual usuario](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-usuario.md)
- [Manual admin](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-admin.md)
- [docs/MODULOS-PRODUCTO.md](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/MODULOS-PRODUCTO.md)
- [Slack canvas Panel FacturaIA](https://agentesialab.slack.com/docs/T0ARXF0V31S/F0AV38CHYSJ)

## Reglas de proyecto

Ver `facturaia/CLAUDE.md` (en repo). Resumen rápido:
- Lint + typecheck + build limpios antes de commit
- Toda tabla nueva = RLS en la misma migración
- Endpoints con superadmin impersonando: `?org_id=` query, no cookie
- Dependencias visibles: módulos premium documentados en `docs/MODULOS-PRODUCTO.md`

## Histórico de hitos

- 2026-05-06: sistema módulos premium completo (catálogo + add-ons + recomendador IA + activity feed + métricas)
- 2026-05-02: integración API v1 ↔ agency-portal (webhooks HMAC, outbox, Stripe-style sync)
- 2026-04-28: presupuestos / proformas / abonos voz + form manual
- 2026-04-27: VeriFACTU integración completa (QR en PDFs, AEAT)
- 2026-04-25: plantillas de factura PDF pixel-perfect
- 2026-04-21: WhatsApp ingesta multi-tenant + Admin Panel + Feature Flags
