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

- **FacturaIA — Presupuestos, Proformas y Abonos completos (2026-04-26)**
  - Ya existe: tabla `presupuestos` con estados propios (borrador/enviado/aceptado/rechazado/expirado/facturado), vista con KPIs, conversión a factura
  - Ya existe: plantillas PDF soportan `tipo: 'factura' | 'presupuesto' | 'proforma' | 'abono'`, serie `P` para presupuestos
  - **PENDIENTE — Fase 1: Presupuestos completos**
    - Conectar formulario `generar-view` con tabla `presupuestos` (ahora solo genera facturas)
    - Serie `P` funcional con `next_invoice_number`
    - PDF de presupuesto descargable/enviable por email
    - Conversión presupuesto → factura ya existe, verificar que copia líneas correctamente
  - **PENDIENTE — Fase 2: Proformas**
    - Nueva tabla `proformas` o campo `documento_tipo` en facturas (decidir)
    - Serie nueva (ej: `F` proforma)
    - Estados: borrador → enviada → pagada → convertida
    - Conversión proforma → factura
  - **PENDIENTE — Fase 3: Abonos (facturas rectificativas)**
    - Campo `factura_origen_id` para vincular abono con factura original
    - Serie `B` para abonos
    - Importes negativos automáticos desde factura original
    - Ajuste de saldo del cliente
    - Cumplimiento fiscal: referencia obligatoria a factura rectificada
  - **PENDIENTE — Fase 4: Vistas y métricas**
    - Pestaña presupuestos conectada al formulario (crear desde ahí)
    - Vistas para proformas y abonos (nuevas pestañas o filtros)
    - Pipeline de ventas: presupuestos → proformas → facturas con trazabilidad
    - Métricas: tasa de conversión, tiempo medio aceptación, importe en pipeline

- **FacturaIA — Generador facturas por voz WhatsApp — SIMPLIFICADO (2026-04-26)**
  - ~~3 sub-workflows + Redis~~ → 1 workflow receptor v2 (`zYcHHa8jWXB6dY5i`) con AI Agent + Postgres Chat Memory
  - ~~`/api/voice/extract`~~ → eliminado, extracción la hace el AI Agent en n8n
  - Flujo e2e funciona: audio → Whisper → AI Agent (consulta catálogo + clientes) → resumen WhatsApp → botones → confirmar → factura creada + PDF generado + PDF enviado por WhatsApp
  - Fixes aplicados: Font.register con rutas absolutas, quitar 'use client' de InvoicePDF, series_numeracion query directa (bypass RLS), multipart formBinaryData para WhatsApp Media upload, template_config por org
  - Fix aplicado (2026-04-26): `template_config: {}` causaba crash PDF para orgs nuevas → merge robusto con defaults en InvoicePDF + orgs nuevas se crean con config completa
  - **PENDIENTE CRÍTICO**:
    1. ~~Verificar que funciona para CADA org (no solo la de test)~~ ARREGLADO — template_config con deep merge + BD parcheada
    2. Comprobar que OCR facturas recibidas sigue funcionando con receptor v2 (rama imagen/documento NO testeada)
    3. Probar rama presupuestos (`tipo: 'presupuesto'`)
    4. **Handler texto libre conectado con FacturaIA** — cuando el usuario escribe texto (ej: "Envíala", consultas, etc.), el bot responde genérico. Necesita: conectar AI assistant para responder consultas sobre facturas, estados, vencimientos, y entender comandos naturales como "envíamela"
  - **PENDIENTE**:
    5. ~~Mejorar textos mensajes WhatsApp~~ EN PROGRESO
    6. **PDF por voz se deforma** — `@react-pdf/renderer` no replica el layout HTML de las plantillas. Investigar migrar a Puppeteer (`/api/render-pdf`) para consistencia
    7. Probar corrección: pulsar "Corregir", enviar texto con cambio, verificar que actualiza y re-muestra botones
    8. Probar cancelación: pulsar "Cancelar", verificar sesión borrada
    9. Actualizar manuales usuario y admin con flujo de voz simplificado
    10. Limpiar facturas duplicadas de testing en BD
- **FacturaIA — Asistente IA conversacional multi-canal (VISIÓN)**
  - Conectar el AI assistant (Claude, ya existe en dashboard) al canal WhatsApp
  - Consultas por WhatsApp/email: facturas vencidas, resúmenes del mes/semana, pagos pendientes de cobro, datos de cuenta, listas, informes
  - Extensiones futuras:
    - Cobrador inteligente: recordatorios automáticos escalonados (amable → formal → urgente) por WhatsApp/email
    - Predicción de cashflow: cuándo paga cada cliente, alertas de liquidez
    - Auto-categorización de gastos recibidos con aprendizaje por org
    - Alertas proactivas: "facturas un 30% menos", "3 vencen esta semana"
    - Generación de presupuestos por contexto: "como el del mes pasado para X pero +10%"
    - Informe fiscal trimestral automático (IVA para gestor)
  - Arquitectura: reutilizar AI assistant route con tool-use para queries a BD, compartir entre canales
- **FacturaIA — Google OAuth email por org (PENDIENTE)**
  - Cada org envia facturas desde su propio email via Google OAuth (no SMTP compartido)
  - Necesita: OAuth token storage per org, Gmail API send, template editor (asunto/cuerpo/firma con variables)
  - Seccion en Settings: "Emails transaccionales" con preview y variables ({{numero}}, {{cliente}}, {{total}})
  - De momento funciona con SMTP centralizado (info@agentesia.madrid) + texto predeterminado con nombre de org
- **FacturaIA — Canales de Ingesta + Plan y Facturación (spec aprobada 2026-04-24)**
  - ~~WhatsApp multi-tenant: matching por número remitente, quitar hardcode n8n~~ HECHO 2026-04-25 — n8n workflows desplegados, código en main
  - Canales de ingesta: rediseño sin toggles, config expandible, banner confirmación, "Mejorar plan" para locked
  - Plan y Facturación: página completa con planes reales, método de pago (UI), historial (mockup)
  - Registro: captura de móvil obligatorio + auto-populate settings
  - Spec: `docs/superpowers/specs/2026-04-24-canales-ingesta-plan-facturacion-design.md`
  - **PENDIENTE**: crear plan de implementación (writing-plans) y ejecutar
- **FacturaIA — Email ingesta con OAuth Gmail COMPLETADO (2026-04-24)**
  - OAuth Gmail conectado y probado e2e, polling configurable por org, boton "Revisar ahora"
  - n8n workflow activo 30min (`dqvzeyeifTcNv50u`), dedup SHA256, timing-safe auth
  - Code review: timing-safe compare, fuente vs origen, JSON.parse try/catch, last_checked fix
  - Manuales actualizados (usuario + admin con referencia visual completa)
  - Precios planes conectados a BD y editables desde admin, CLAUDE.md con regla manuales
- **FacturaIA — pendientes anteriores**
  - ~~Verificar visualmente facturas emitidas/recibidas en navegador~~ HECHO 2026-04-25 — UI redesign completo
  - Deploy a producción (push + Dokploy redeploy + Traefik reload), test e2e OCR en prod
  - ~~Actualizar manuales usuario/admin con cambios de UI~~ HECHO 2026-04-25 — manuales actualizados con envío email, filtros borrador/enviada, nuevo formulario, catálogo
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
  - ~~**PENDIENTE**: probar toggle features por org (override vs plan default), toggle features por plan, editar limites~~ HECHO 2026-04-25 — limits tab corregida (ilimitado, storage real, invalidación cache al cambiar plan)
  - ~~**PENDIENTE**: verificar billing banner (trial/grace/expired), feature gates (`<Feature>`)~~ HECHO 2026-04-26 — banner rediseñado con 3 variantes (info/warn/danger), iconos SVG, OKLCH, responsive. FeatureLocked con badge + layout vertical
  - ~~**PENDIENTE**: verificar lazy expiration (billing state machine: trial → grace_period → expired)~~ HECHO 2026-04-26 — código verificado (8 tests pasan), RPC validada, UI rediseñada
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
- **Clínica Zen — cancelar cita debe borrar evento Calendar** — workflow `DkueIeGFWLKh8nTj` cambia status en Kommo pero no borra/modifica evento en Google Calendar. Añadir nodo Delete/Update Event
- **Clínica Zen — configurar Retell en workflow leads entrantes** (`RN0wl8RaRmwLpnfQ`) — verificar webhooks apuntan a dominio CZ correcto (no EasyPanel viejo), configurar agente voz CZ
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte`
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- ~~Clinica Zen: scope "Chats" de Kommo~~ DESCARTADO — no disponible

## Completado reciente

- FacturaIA: billing banner + feature-locked rediseñados (2026-04-26) — banner con 3 variantes (info/warn/danger), iconos SVG por estado, colores OKLCH, responsive (oculta detalle en mobile). FeatureLocked con badge icono + layout vertical + text link CTA. Lazy expiration verificada (8 tests, RPC validada)
- FacturaIA: datos fiscales completos en clientes y proveedores (2026-04-26) — migración 013 añade cp, pais a clientes y telefono, ciudad, direccion, cp, pais a proveedores. Modal de edición funcional (antes decía "Próximamente"). Cards muestran dirección. Generar-view pasa dirección/cp al receptor del PDF. Voice: schema, insert y prompt del AI Agent actualizados para extraer y guardar datos fiscales del audio. Tool consultar_clientes devuelve 9 campos (antes 4). Manuales actualizados
- FacturaIA: simplificación workflow voz WhatsApp (2026-04-26) — 3 sub-workflows + Redis → 1 AI Agent con Postgres Chat Memory. Eliminados: voice-process, voice-confirm, voice-correct, `/api/voice/extract`. Flujo e2e funciona: audio → Whisper → agente → resumen → botones → confirmar → factura + PDF por WhatsApp. Fixes: Font.register rutas absolutas, 'use client' eliminado de InvoicePDF, series bypass RLS, multipart formBinaryData, template_config por org. PENDIENTE: verificar multi-org, OCR, presupuestos, textos mensajes, manuales
- FacturaIA: rediseño formulario nueva factura + envío email (2026-04-25) — formulario con tarjetas, catálogo con autocompletado por categoría, descripción separada en plantillas, guardar borrador vs guardar y enviar, email auto-send al cliente, campo email para clientes sin email (guarda en cliente), opción "Enviar por email" en menú 3 puntos de emitidas, filtros Borrador/Enviada, migración email_envio, API /api/email/send con Nodemailer SMTP, manuales actualizados
- FacturaIA: generador facturas por voz — n8n workflows desplegados (2026-04-25) — 3 sub-workflows (voice-process, voice-confirm, voice-correct) importados y activos en n8n.agentesia.world, receptor actualizado con routing de voz (31 nodos), OpenAI GPT-4o para extracción, Whisper con credencial OpenAI. Migración 010+011 ejecutadas. PENDIENTE: redeploy Dokploy + OPENAI_API_KEY en env + test e2e
- FacturaIA: system_config + admin config page (2026-04-25) — tabla system_config (key-value JSONB), página /admin/config con número global WhatsApp editable (protegido por re-auth con contraseña), migración 011 ejecutada
- FacturaIA: security hardening (2026-04-25) — auth en render-pdf, timingSafeEqual en generate-pdfs, whitelist métodos en impersonate query + audit log, rate limiting in-memory (upload 20/min, AI 30/min), magic number validation en uploads, sanitizado errores internos en respuestas API
- FacturaIA: plantillas de factura con PDF pixel-perfect (2026-04-25) — 4 plantillas (Tech, Corp, Freelance, Creativa), selección en Settings, preview HTML en tiempo real, descarga PDF via Puppeteer (`/api/render-pdf`) idéntico al preview. Soporte para tipo de documento (Factura/Presupuesto/Proforma/Abono). Browser singleton warm ~2.3s
- FacturaIA: admin limits/storage fix (2026-04-25) — limits tab muestra "Ilimitado" para enterprise (no 99999), storage_mb calculado en tiempo real via Storage SDK (no columna estática), cache de limits se invalida al cambiar plan, conteos facturas+bandeja visibles en tab General
- FacturaIA: UI improvements (2026-04-25) — filtros minimalistas con "Más filtros" colapsable, month rows compactos (-50% altura), sin_aprobar pinned arriba en recibidas, auto-logos proveedores (Google Favicon API con sentinel not_found), preview modal ajustada (max-height + fullscreen móvil), mobile responsive completo. Migración 008 (logo_url) ejecutada en Supabase Cloud.
- Obsidian inbox procesado: 25→1 notas, 3 promocionadas a knowledge/, 2 tareas añadidas (2026-04-25)
- FacturaIA: vitest configurado con 22 tests para billing, features y admin (2026-04-25)
- FacturaIA: complimentary orgs — campo boolean, MRR excluye complimentary, estrella morada en admin, toggle en billing tab (2026-04-25)
- FacturaIA: KPI cards y status cards clickables en admin dashboard, navegan a orgs/plans con filtro por status (2026-04-25)
- FacturaIA: Email Ingesta OAuth Gmail completo (2026-04-24) — OAuth connect/disconnect, polling configurable por org (1h/2h/6h/12h/24h), boton "Revisar ahora", dedup SHA256, timing-safe auth, code review fixes, manuales actualizados, precios planes dinámicos desde BD, Slack canvas actualizado
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
