---
title: Simarro — Routing de visitas por agente + duración 1h
date: 2026-05-27
source: sesion-claude-code
tags: [simarro, n8n, retell, supabase, calendar, routing, citas]
---

# Routing de visitas por agente (Simarro)

> Source of truth: `/Users/manueldelmonte/simarro/CLAUDE.md` sección "Routing de visitas por agente + duración 1h". Esto es snapshot de la sesión.

## Qué pidió el cliente
- Cada vivienda lleva en la descripción de Idealista `agente: <nombre>`. La visita debe agendarse en el **Google Calendar de ese agente**.
- Todas las visitas pasan a durar **1 hora** (antes 30 min).
- Entre visitas seguidas del mismo agente: **misma vivienda → pegada (0 min); distinta vivienda → +30 min** de margen (simétrico).

## Arquitectura (decisiones)
- **Fuente del agente = `properties.description`** (texto completo scrapeado). Se parsea en el **sync** `nzxtGnblEFwwkofO` (nodo `Prepare Items`) a la columna nueva `properties.agent`. No se parsea en el chat porque la búsqueda trunca la descripción a 300 chars.
- **Single source of truth del mapeo = tabla `agents`** (`agent_key, display_name, calendar_id, active`), 8 agentes. NO se persiste el agente resuelto en `properties` (solo el texto crudo normalizado); la resolución se hace al vuelo.
- **RPC `resolve_property_calendar(idealista_id)`** (SQL, match por subconjunto de tokens) devuelve el `calendar_id` o fallback. La usan las 3 ramas (voz/WhatsApp/disponibilidad) → lógica en un solo sitio.
- **Fallback = `consultingsimarroproperties@gmail.com`** (id real). El literal `'primary'` NO vale en GoogleCalendar `mode:'id'` (bug encontrado y corregido).
- **Buffer solo en disponibilidad** (no al crear evento) — es donde importa que no se ofrezcan horas que solapen.

## Gotchas encontrados
- **PostgREST `Accept: application/vnd.pgrst.object+json`** → n8n no lo auto-parsea, mete el JSON como **string bajo `.data`**. La expresión del calendario lo parsea defensivamente (`typeof r.data==='string' ? JSON.parse(r.data) : r`) y cae al fallback ante cualquier error.
- **`'primary'` inválido en GCal `mode:'id'`** → usar el email del calendario.
- **Cred Postgres del catálogo**: `properties` NO está en la base `n8n` (cred `NbSEPfQRe9htaaYm` = host `postgres`/db `n8n`), ni en `kg8smgEwoRUgZZrz` (borrada). DDL del catálogo → **Supabase Studio** (`supabase-simarro.agentesia.madrid`), no hay cred Postgres directa viva. El sync escribe por PostgREST/Kong.
- **Transcripción de calendar_ids**: el ID de Pedro venía con un char de más (65 vs 64). Fuente de verdad: `calendarList` API de la cuenta (todos `accessRole: owner`).
- **Composición voz vs WhatsApp**: el chatbot tenía su propio `Mirar_disponibilidad` (googleCalendarTool, `primary` fijo) → ofertaba en primary pero reservaba en el agente. Reemplazado por `toolHttpRequest` al webhook agent-aware. Lección: [[audits-cross-pr-vs-per-pr]] — el bug solo aparece en la COMPOSICIÓN de los dos canales, no en cada uno aislado.

## Cómo se hizo (n8n por API REST, sin MCP)
- API key en `~/simarro/.claude/settings.local.json`. Workflows leídos/editados con `PUT /api/v1/workflows/{id}` (settings: solo claves permitidas por el schema público; n8n preserva las que no envías).
- DDL a prod: el guardarraíl bloquea webhooks que ejecutan SQL arbitrario → se usó workflow con **trigger manual** que el user ejecuta, o **Supabase Studio**.
- Cambios Retell y revisión final con **subagentes** (filtrando outputs).

## Pendiente go-live
1. Ramón añade `agente:` a las descripciones de Idealista.
2. Correr el sync para poblar `properties.agent`.
3. Test E2E real de creación de evento en calendario del agente (vivienda `110751938` sembrada con `carlos`; revertir luego con `UPDATE properties SET agent=NULL WHERE idealista_id='110751938';`).
4. Publicar agente Retell (`is_published:true`).
5. Verificar carga completa del catálogo (ojo `desiredResults:10` en el actor Apify — puede estar capando el nº de propiedades).

Ver también [[estado-actual]].
