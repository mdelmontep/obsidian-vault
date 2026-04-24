---
title: top of mind
date: 2026-04-20
tags: [home, prioridades]
---

# Top of Mind

## URGENTE

- **Clinica Zen — Corregir email de confirmación (2026-04-25)**
  - Las imágenes (hero + logo) se subieron como base64 inline pero hay que verificar que cargan en Gmail/Apple Mail
  - Probar enviando un formulario de test y comprobar el email recibido
  - Workflow: `13Roz21TOBwy8gp8` en `n8nclinicazen.agentesia.madrid`
  - Nodo: `Send Confirmation Email`
  - Si base64 no funciona en algún cliente, buscar alternativa (Cloudinary o similar)

## Prioridades esta semana

- **FacturaIA — Canales de Ingesta + Plan y Facturación (spec aprobada 2026-04-24)**
  - WhatsApp multi-tenant: matching por número remitente, quitar hardcode n8n
  - Canales de ingesta: rediseño sin toggles, config expandible, banner confirmación, "Mejorar plan" para locked
  - Plan y Facturación: página completa con planes reales, método de pago (UI), historial (mockup)
  - Registro: captura de móvil obligatorio + auto-populate settings
  - Spec: `docs/superpowers/specs/2026-04-24-canales-ingesta-plan-facturacion-design.md`
  - **PENDIENTE**: crear plan de implementación (writing-plans) y ejecutar
- **FacturaIA — Email ingesta con OAuth Gmail (PRIORITARIO)**
  - Fase 2 de canales de ingesta: conectar Gmail del cliente vía OAuth, un solo workflow n8n pollea todas las orgs cada 5 min, extrae adjuntos PDF/imagen y manda al pipeline OCR
  - Requiere: registrar app en Google Cloud Console, endpoint callback, workflow n8n con loop
  - **PENDIENTE**: implementar después de la tanda actual de canales de ingesta
- **FacturaIA — pendientes anteriores**
  - Verificar visualmente facturas emitidas/recibidas en navegador
  - Deploy a producción (push + Dokploy redeploy + Traefik reload), test e2e OCR en prod
- ~~Mover repos de AgentesIAMadrid a cuenta personal GitHub~~ PARCIAL — `obsidian-vault` movido a `mdelmontep/obsidian-vault` (privado)
- **Clinica Zen — chatbot + voz COMPLETADO (2026-04-23)**:
  - Chatbot WhatsApp (prompt v7) + Agente Retell (prompt v8) — ambos en producción
  - Teléfono definitivo conectado, agente publicado
  - Salesbot 68822 corregido (acción mover leads eliminada)
  - RAG Supabase verificado
  - Scope "Chats" Kommo descartado — no se puede habilitar, se mantiene amojo token manual
  - **Limitación conocida**: amojo_token expira ~24h, hay que actualizarlo manualmente
- **FacturaIA — Admin Panel + Feature Flags (implementado 2026-04-21)**
  - 24 tareas completadas, código en main, push hecho
  - Migración `004_admin_feature_flags.sql` ejecutada en Supabase — 8 tablas, 6 funciones SQL, RLS, seed (3 planes, 27 features, 60 plan_features)
  - ~~**PENDIENTE INMEDIATO**: probar en navegador~~ HECHO 2026-04-21 — admin orgs/features/plans carga OK tras fix Zod v3
  - ~~**PENDIENTE**: impersonate banner (`?impersonate=org_id`)~~ HECHO 2026-04-22 — full impersonation con proxy client, banner animado, todas las páginas migradas
  - **PENDIENTE**: probar toggle features por org (override vs plan default), toggle features por plan, editar limites
  - **PENDIENTE**: verificar billing banner (trial/grace/expired), feature gates (`<Feature>`)
  - **PENDIENTE**: verificar lazy expiration (billing state machine: trial → grace_period → expired)
  - **PENDIENTE**: tests — no hay tests automatizados aun, considerar al menos tests para `orgHasFeature`, `getOrgBilling`, `isSuperadmin`
  - **NOTA**: `profiles` tabla vacia — superadmin funciona via `SUPERADMIN_EMAILS` env var. Cuando haya signup real, el trigger insertara en profiles
  - Archivos clave: `src/lib/admin.ts`, `src/lib/features.ts`, `src/lib/billing.ts`, `src/providers/feature-provider.tsx`, `src/providers/billing-provider.tsx`, `src/app/(admin)/`
  - Spec: `docs/superpowers/specs/2026-04-21-admin-feature-flags-design.md`
  - Plan: `docs/superpowers/plans/2026-04-21-admin-feature-flags.md`
- **FacturaIA — WhatsApp ingesta + Canales de Ingesta UI (completado 2026-04-21)**
  - WhatsApp Cloud API conectado: webhook per-phone-number override (no rompe Chatwoot compartido)
  - n8n workflows: `whatsapp-verify` (GET) + `whatsapp-receptor` (POST) con OCR pipeline
  - Multi-tenant: lookup org por `settings.whatsapp.phone_number_id`
  - Phone normalization: strip +34, espacios, guiones — match bidireccional
  - Registro con telefono, config WhatsApp en settings y admin panel
  - UI "Canales de Ingesta" en pagina Agentes IA: 4 cards (WhatsApp, Dashboard, Email, Telegram)
  - Conectado a FeatureProvider (useFeatures hook, no RPCs individuales)
  - Toggle persiste en settings.canales JSONB, stats reales desde bandeja_ingesta
  - Estados: activo (borde color canal), inactivo (opacity), locked (badge Upgrade)
  - Audit frontend aplicado: accesibilidad toggle, pills rgba() dark mode, race condition fix, skeleton loading
  - Commit `ab58feb`, pusheado a main
- **FacturaIA — Conciliación bancaria con IA (spec aprobada 2026-04-21)**
  - Spec completa en `docs/superpowers/specs/2026-04-21-conciliacion-bancaria-design.md`
  - 5 tablas nuevas, pipeline Claude 2 fases, UI con aprobación por lotes
  - Manuales usuario y admin actualizados
  - **PENDIENTE**: crear plan de implementación (writing-plans) y ejecutar
- **Tecnocloud — configurar WhatsApp en FacturaIA** — schema arreglado (telefono + settings), falta obtener phone_number_id de Meta, guardarlo en org, configurar webhook override
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte`
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- ~~Clinica Zen: scope "Chats" de Kommo~~ DESCARTADO — no disponible

## Completado reciente

- FacturaIA: WhatsApp multi-tenant matching corregido (2026-04-24) — matching por número remitente en vez de phone_number_id, sincronización telefono→settings.whatsapp.phone_number en settings, admin PATCH y auto-populate frontend
- n8n.agentesia.world: compose corregido con healthcheck HTTP, pruning ejecuciones, memory limit 2G, versión fija 2.15.1 (2026-04-22). Compose guardado en `~/n8n-agentesia-world-compose.yml`
- FacturaIA: adminUpdateOrgSchema ampliado con `telefono` y `settings` — fix Zod `.strict()` que impedía guardar WhatsApp config desde admin (2026-04-22)
- FacturaIA: Full impersonation (2026-04-22) — proxy client que bypassa RLS via admin client, cookie-based middleware, todas las vistas migradas de createClient a useOrgClient hook, banner animado OKLCH, modal previsión de gastos. Settings muestra datos admin (pendiente migrar sub-componentes). Commit `a7f6161`.
- FacturaIA: Tanda 2 + Tanda 3 de Borja mergeadas a main (2026-04-21) — tokens CSS semánticos, focus ring, fuentes Filson en PDFs, empty states, skeletons, disabled styles, a11y (aria-labels), drop-zone mejorada. Issues: mobile responsive pendiente, preview PDF en Generar con campos apilados/fuera de posición. Test completo en [[facturaia-test-tanda-2-3]]
- FacturaIA: fix Zod v3 syntax (z.email→z.string().email, z.uuid→z.string().uuid, z.iso.datetime→z.string().datetime) — rompía todas las API routes admin
- FacturaIA: canales de ingesta conectados a FeatureProvider (useFeatures hook) — eliminada duplicación de RPCs que causaba tarjetas bloqueadas con plan correcto
- FacturaIA: ID de org visible (read-only) en admin panel, tab General
- FacturaIA: 5 tests manuales de seguridad verificados — email registro OK, XSS neutralizado, duplicado detectado, .txt rechazado, campos id/created_at no editables
- FacturaIA: WhatsApp ingesta + Canales de Ingesta UI — webhook per-phone-number, n8n receptor+verify, multi-tenant por phone_number_id, 4 cards con feature flags, toggle JSONB sin race condition, audit frontend (a11y, dark mode pills, skeleton)
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
- FacturaIA: CLAUDE.md por proyecto creado con 20 reglas específicas (schema, frontend, auth, OCR, repo)
- CLAUDE.md global optimizado: 199→157 líneas. Gotchas movidos a Stack/ y facturaia/CLAUDE.md. SMTP movido a memory.
- FacturaIA: manuales usuario y admin actualizados con sección Banco
