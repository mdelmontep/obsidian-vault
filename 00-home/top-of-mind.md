---
title: top of mind
date: 2026-04-17
tags: [home, prioridades]
---

# Top of Mind

## Prioridades esta semana

- ~~Mover repos de AgentesIAMadrid a cuenta personal GitHub~~ PARCIAL — `obsidian-vault` movido a `mdelmontep/obsidian-vault` (privado). Remote local, CLAUDE.md, hot.md y Daily Briefing trigger actualizados. **Pendiente**: decidir si mover más repos (facturaia descartado por ahora)
- **FacturaIA — dashboard facturación** — Fases 1-5 completadas. Dashboard 100% funcional con datos reales Supabase (KPIs, sparklines, cashflow SVG, donut, alertas dinámicas). CRUD completo facturas (editar, eliminar, filtros, CSV export, bulk actions). Ingesta IA con OCR pipeline funcionando (n8n + GPT-4o-mini Vision + Realtime). Deploy en facturaia.agentesia.world. **Pendiente**: test e2e OCR en producción, deploy automático (webhook GitHub→Dokploy), developer dashboard `/admin`
- ~~BLOQUEANTE Clinica Zen: Google Calendar ID incorrecto~~ RESUELTO — ID confirmado correcto por el usuario. Si Recordatorios falla, el problema es la credencial OAuth (Cuenta Gonzalo), no el ID
- **Clinica Zen — pendientes post-migración**:
  - ~~Añadir nodo Create Event en Leads entrantes~~ HECHO
  - Cambiar Google Calendar ID en TODOS los workflows (chatbot, leads entrantes, especialista, recordatorios)
  - ~~Verificar que SMTP `citas@clinicazen.es` funciona~~ HECHO — credencial yJGBBnGxWMImvH1x creada y verificada
  - Cancelación de cita debe borrar evento del calendario (no implementado)
  - Revisar agente de voz Retell: webhooks pueden apuntar al EasyPanel viejo
  - Verificar contenido RAG (Supabase) actualizado para CZ — Google Doc fuente es privado y credencial Drive puede ser de gonzalo
  - ~~Confirmar task type "Cita asignada" con Gonzalo~~ HECHO — es "Especialista asignado"
- **Clinica Zen: Chatbot prompt v7 aplicado — pendiente test real WhatsApp** (confirmación con día semana, STOP antes de Reservar_cita, anti-invención disponibilidad, onError continueErrorOutput)
- **Clinica Zen: Configurar agente de voz Retell** en workflow Leads entrantes — webhooks pueden apuntar a EasyPanel viejo, verificar URLs y config
- **Clinica Zen: Test cancelar/cambiar cita** — flujo completo sin probar, cancelación no borra evento Calendar (pendiente implementar)
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte` con Bot incidencias
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- ~~FacturaIA: SQL schema no ejecutado~~ RESUELTO — schema ejecutado, 17 tablas + RLS multi-tenant + funciones SECURITY DEFINER operativas
- ~~Clinica Zen: Calendar ID no accesible~~ RESUELTO — ID confirmado correcto
- Clinica Zen: pendiente scope "Chats" de Kommo (contactar soporte) — bloquea patrón Laserys para amojo_token dinámico

## Completado reciente

- Chatbot CZ prompt v7: confirmación con día semana + STOP antes de Reservar_cita + anti-invención disponibilidad
- Todos los emails `info@hiflymadrid.com` → `citas@clinicazen.es` en todos los workflows CZ
- Todos los `status_id` de gonzalo migrados a CZ
- Especialista Asignado completo: webhook Kommo + IF anti-duplicados + field names + Calendar+Tasks+Email
- toolWorkflow `onError: continueErrorOutput` en los 4 nodos tool del chatbot
- Workflow archivado "Agente de Voz Clinica Zen" eliminado (no era de CZ)
- FacturaIA Fases 1-5 completadas: dashboard con datos reales, CRUD facturas, ingesta IA con OCR, deploy funcional en facturaia.agentesia.world
- SMTP citas@clinicazen.es verificado y funcional (cred yJGBBnGxWMImvH1x, mail.clinicazen.es:465)
- Chatbot CZ prompt v3: 3 bugs críticos corregidos (fecha domingo→lunes, 0 eventos=todo libre, Reservar_cita forzado) + investigación mejores prácticas aplicada
- Todas las credenciales de workflows CZ verificadas (Calendar, Kommo, SMTP)
- Auditoría completa flujo de reserva CZ: 5 issues críticos encontrados y corregidos (Calendar Create, token gonzalo en Recordatorios, filtro timeMin/timeMax, emails kevinrcuenca14 → info@hiflymadrid.com)
- Migración completa 9 workflows Clinica Zen + fix chatbot flooding
- Setup completo Obsidian + Claude Code + Daily Briefing + Slack bot
- Cerebro conectado: CLAUDE.md reducido de 442 a ~145 líneas (~80% menos tokens/turno). Reglas especializadas migradas a 11 archivos en Stack/. Lectura automática de vault por tema configurada
