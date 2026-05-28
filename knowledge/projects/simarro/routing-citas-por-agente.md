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
- **LLM omite `idealista_id` en `Mirar_disponibilidad`** (bug detectado 2026-05-28): el LLM tenía el `idealista_id` del resultado de `Buscar_viviendas` pero no lo pasaba a `Mirar_disponibilidad` → RPC devolvía `source=fallback` → disponibilidad consultada en calendario general → slots del agente aparecían libres → double booking. La REGLA CRÍTICA en `tools_gating` no era suficiente; añadida también en el nodo BUSCANDO del state machine con "CRÍTICO: sin idealista_id el sistema consulta el calendario equivocado". Ver [[audits-cross-pr-vs-per-pr]].
- **Teléfono voz sin E.164 → WA no llega** (bug detectado 2026-05-28): `from_number` de Retell llega como "+34617314938" pero el workflow lo strip a "617314938" antes de guardar en Kommo. Kommo/Meta necesita E.164 para identificar la cuenta WA del contacto nuevo → 3108 silencioso. Fix: `Create new contacts1` en `iMoTKZWxYLymGuHF` normaliza ahora el teléfono a `+34XXXXXXXXX`. Afecta solo a contactos NUEVOS (primera llamada); contactos creados por WA ya tienen E.164 de Kommo.
- **LLM hallucina preguntas RGPD** (bug detectado 2026-05-28): step "Consentimiento WhatsApp" sin freno → el LLM improvisa "¿Quieres que te mande la información legal de protección de datos?". Fix: añadido PROHIBIDO explícito con lista de términos vetados (RGPD, privacidad, legal, información legal).

## Cómo se hizo (n8n por API REST, sin MCP)
- API key en `~/simarro/.claude/settings.local.json`. Workflows leídos/editados con `PUT /api/v1/workflows/{id}` (settings: solo claves permitidas por el schema público; n8n preserva las que no envías).
- DDL a prod: el guardarraíl bloquea webhooks que ejecutan SQL arbitrario → se usó workflow con **trigger manual** que el user ejecuta, o **Supabase Studio**.
- Cambios Retell y revisión final con **subagentes** (filtrando outputs).

## Pendiente go-live

### Bloqueante — depende de Ramón
1. Ramón añade `agente:` a las descripciones de Idealista (actualmente `properties.agent = NULL` en todas → fallback siempre al calendario general).
2. Correr el sync (`Lanzar scrape Simarro (manual)`, workflow `3zBDpPwBYLZgMink`) para poblar `properties.agent`.
3. Test E2E real: llamada voz → vivienda con agente → `Mirar_disponibilidad` devuelve `source=agent` en n8n log → cita en calendario del agente.

### Técnico pendiente
4. Revertir vivienda de test: `UPDATE properties SET agent=NULL WHERE idealista_id='110751938';`
5. Limpiar eventos de test en Google Calendar (Julián 12:00, Juan 12:00 del 29 mayo).
6. Publicar agente Retell: `PATCH /update-agent/agent_7b02aa7680b8798ea033fab2c2` con `is_published: true`.

### Verificado ✓ (tests 2026-05-28)
- WA confirmación llega para contactos nuevos de voz ✓
- Ana no pregunta "mañana o tarde" si el cliente ya dio hora ✓
- Ana no improvisa preguntas RGPD ✓
- `Mirar_disponibilidad` pasará el `idealista_id` al calendario correcto (fix aplicado, pendiente E2E con propiedad con agente real)

Ver también [[estado-actual]].
