---
title: top of mind
date: 2026-04-20
tags: [home, prioridades]
---

# Top of Mind

## Prioridades esta semana

- **FacturaIA — sesión larga de mejoras en curso** — calendario interactivo, cashflow con negativos, pills con pulso, filtros por rango de fechas, settings de apariencia (colores, tipografía Mermaid, pills, categorías), smart alerts, top proveedores, previsión de gastos fijos. Seed con 60 facturas realistas + PDFs generados con pdf-lib.
  - **PENDIENTE INMEDIATO**: verificar visualmente en navegador que las facturas emitidas muestran nombres de clientes (datos OK en BD, falta hard refresh), verificar recibidas distribuidas correctamente entre proveedores, probar click en número de factura para previsualizar PDF
  - **PENDIENTE**: deploy a producción (push + Dokploy redeploy + Traefik reload), test e2e OCR en prod
- ~~Mover repos de AgentesIAMadrid a cuenta personal GitHub~~ PARCIAL — `obsidian-vault` movido a `mdelmontep/obsidian-vault` (privado)
- **Clinica Zen — agente de voz funcional (2026-04-20)**:
  - Agente Retell probado con llamada real (Julián Fernández). Reserva completada OK
  - Code Node disponibilidad ARREGLADO — consulta calendario real
  - Ruta contacto existente ARREGLADA — ya no falla Append row
  - Prompt Retell v8 — "una pregunta cada vez" reforzado
  - Calendar events con formato limpio (summary + description)
  - 15 eventos test creados para semana 21-25 abril
  - **Pendiente**: conectar teléfono definitivo en Retell + publicar agente
  - **Pendiente**: cancelación de cita debe borrar evento Calendar (no implementado)
  - **Pendiente**: test cambiar fecha (mover evento)
  - **Pendiente**: verificar RAG Supabase actualizado
  - **Pendiente**: scope "Chats" Kommo → token dinámico
- **FacturaIA — Admin Panel + Feature Flags (implementado 2026-04-21)**
  - 24 tareas completadas, código en main, push hecho
  - Migración `004_admin_feature_flags.sql` ejecutada en Supabase — 8 tablas, 6 funciones SQL, RLS, seed (3 planes, 27 features, 60 plan_features)
  - **PENDIENTE INMEDIATO**: probar en navegador (`npm run dev`) — login → verificar que sidebar filtra features → ir a `/admin` → probar dashboard KPIs, orgs list, org detail (6 tabs), features catalog, plans editor, alerts
  - **PENDIENTE**: verificar billing banner (trial/grace/expired), feature gates (`<Feature>`), impersonate banner (`?impersonate=org_id`)
  - **PENDIENTE**: probar toggle features por org (override vs plan default), toggle features por plan, editar limites
  - **PENDIENTE**: verificar lazy expiration (billing state machine: trial → grace_period → expired)
  - **PENDIENTE**: tests — no hay tests automatizados aun, considerar al menos tests para `orgHasFeature`, `getOrgBilling`, `isSuperadmin`
  - **NOTA**: `profiles` tabla vacia — superadmin funciona via `SUPERADMIN_EMAILS` env var. Cuando haya signup real, el trigger insertara en profiles
  - Archivos clave: `src/lib/admin.ts`, `src/lib/features.ts`, `src/lib/billing.ts`, `src/providers/feature-provider.tsx`, `src/providers/billing-provider.tsx`, `src/app/(admin)/`
  - Spec: `docs/superpowers/specs/2026-04-21-admin-feature-flags-design.md`
  - Plan: `docs/superpowers/plans/2026-04-21-admin-feature-flags.md`
- **FacturaIA — Conciliación bancaria con IA (spec aprobada 2026-04-21)**
  - Spec completa en `docs/superpowers/specs/2026-04-21-conciliacion-bancaria-design.md`
  - 5 tablas nuevas, pipeline Claude 2 fases, UI con aprobación por lotes
  - Manuales usuario y admin actualizados
  - **PENDIENTE**: crear plan de implementación (writing-plans) y ejecutar
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte`
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- Clinica Zen: pendiente scope "Chats" de Kommo (contactar soporte)

## Completado reciente

- FacturaIA: Admin Panel + Feature Flags completo — 24 tareas, 8 tablas Supabase, 13 API routes, 5 páginas admin (dashboard, orgs, features, plans, alerts), providers (FeatureProvider fail-open + BillingProvider), billing state machine con lazy expiration, feature gates en sidebar, impersonate banner, middleware admin
- FacturaIA: 60 facturas seed (40 emitidas, 20 recibidas) con distribución round-robin de clientes/proveedores
- FacturaIA: 60 PDFs profesionales generados con pdf-lib y subidos a Supabase Storage
- FacturaIA: calendario interactivo con filtros, approve de sin_aprobar, click para navegar a factura
- FacturaIA: filtro por rango de fechas con 7 presets (esta semana, mes, trimestre, año, anteriores)
- FacturaIA: pills con pulso (rojo vencidas/cerca vencimiento, verde cerca cobro)
- FacturaIA: cashflow chart arreglado para valores negativos
- FacturaIA: settings apariencia funcional (brand colors, tipografía incluyendo Mermaid, pill colors, categorías)
- FacturaIA: panel previsión gastos fijos en dashboard (6 gastos recurrentes seeded)
- FacturaIA: top proveedores y smart alerts (5 tipos) en dashboard
- FacturaIA: número de factura clickeable para previsualizar PDF en modal
- FacturaIA: tabla facturas con layout fijo para evitar columnas cortadas
- FacturaIA: proveedores 3-dot menu arreglado con createPortal
- FacturaIA: donut chart "Estado de facturación" arreglado (faltaba estado enviada)
- FacturaIA: fuente Mermaid añadida como opción de tipografía
- Agente de voz Retell CZ creado via API
- Chatbot CZ prompt v7 completado
- FacturaIA Fases 1-5 completadas
- FacturaIA: rediseño visual completo — paleta azul profesional (#3D7BF5/#1B2B4B), gradientes eliminados, radios reducidos, subtítulos innecesarios quitados, countUp eliminado, font Filson Soft
- FacturaIA: columna acciones (3-dot menu) alineada entre emitidas y recibidas — anchos condicionales con clase .has-origen
- FacturaIA: icono WhatsApp reemplazado por logo oficial, "camara" renombrado a "manual" (código + BD)
- FacturaIA: spec completa conciliación bancaria con IA — modelo de datos, pipeline Claude, prompts optimizados para banca española, UI consistente
- FacturaIA: manuales usuario y admin actualizados con sección Banco
