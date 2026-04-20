---
title: top of mind
date: 2026-04-17
tags: [home, prioridades]
---

# Top of Mind

## Prioridades esta semana

- **FacturaIA — dashboard facturación** — Fase 1 frontend completa (12 vistas). BLOQUEADO: ejecutar SQL schema (17 tablas + RLS) en Supabase Dashboard antes de continuar con Fase 2 (CRUD real). Luego quedan Fases 3-6
- ~~BLOQUEANTE Clinica Zen: Google Calendar ID incorrecto~~ RESUELTO — ID confirmado correcto por el usuario. Si Recordatorios falla, el problema es la credencial OAuth (Cuenta Gonzalo), no el ID
- **Clinica Zen — pendientes post-migración**:
  - ~~Añadir nodo Create Event en Leads entrantes~~ HECHO
  - Cambiar Google Calendar ID en TODOS los workflows (chatbot, leads entrantes, especialista, recordatorios)
  - ~~Verificar que SMTP `citas@clinicazen.es` funciona~~ HECHO — credencial yJGBBnGxWMImvH1x creada y verificada
  - Cancelación de cita debe borrar evento del calendario (no implementado)
  - Revisar agente de voz Retell: webhooks pueden apuntar al EasyPanel viejo
  - Verificar contenido RAG (Supabase) actualizado para CZ — Google Doc fuente es privado y credencial Drive puede ser de gonzalo
  - ~~Confirmar task type "Cita asignada" con Gonzalo~~ HECHO — es "Especialista asignado"
- **Clinica Zen: Chatbot prompt v3 aplicado — pendiente test real WhatsApp** (3 bugs críticos corregidos: fecha incorrecta, calendario vacío, Reservar_cita no ejecutado)
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte` con Bot incidencias
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- **FacturaIA: SQL schema no ejecutado** — `supabase/migrations/001_schema.sql` y `002_rls.sql` escritos pero no aplicados a Supabase Cloud (lahqlyaxvobqjgdiftag). Sin psql ni CLI local. Ejecutar en Dashboard SQL Editor
- ~~Clinica Zen: Calendar ID no accesible~~ RESUELTO — ID confirmado correcto
- Clinica Zen: pendiente scope "Chats" de Kommo (contactar soporte) — bloquea patrón Laserys para amojo_token dinámico

## Completado reciente

- SMTP citas@clinicazen.es verificado y funcional (cred yJGBBnGxWMImvH1x, mail.clinicazen.es:465)
- Chatbot CZ prompt v3: 3 bugs críticos corregidos (fecha domingo→lunes, 0 eventos=todo libre, Reservar_cita forzado) + investigación mejores prácticas aplicada
- Todas las credenciales de workflows CZ verificadas (Calendar, Kommo, SMTP)
- Auditoría completa flujo de reserva CZ: 5 issues críticos encontrados y corregidos (Calendar Create, token gonzalo en Recordatorios, filtro timeMin/timeMax, emails kevinrcuenca14 → info@hiflymadrid.com)
- Migración completa 9 workflows Clinica Zen + fix chatbot flooding
- Setup completo Obsidian + Claude Code + Daily Briefing + Slack bot
- Cerebro conectado: CLAUDE.md reducido de 442 a ~145 líneas (~80% menos tokens/turno). Reglas especializadas migradas a 11 archivos en Stack/. Lectura automática de vault por tema configurada
