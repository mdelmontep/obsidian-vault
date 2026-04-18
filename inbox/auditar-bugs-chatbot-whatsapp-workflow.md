---
title: auditar workflow ChatBOT Agentesia (WhatsApp) para los mismos 3 bugs del Web Chat
date: 2026-04-15
source: claude-code-session
tags: [inbox, pendiente, agentesia, n8n, whatsapp, chatbot, bug]
---

El workflow `ChatBOT - Agentesia` de WhatsApp (ID `enVlCyi7McKfwkRQ`, producción en `n8n.agentesia.madrid`) **probablemente tiene los mismos 3 bugs que se arreglaron en el workflow Web Chat Agentesia** el 2026-04-15, porque el workflow Web fue creado duplicando la configuración del de WhatsApp.

Los 3 bugs fueron descubiertos al testear el workflow Web. No se arreglaron en el de WhatsApp porque el usuario pidió explícitamente no tocar el WhatsApp en esa sesión. Hay que decidir cuándo auditarlo y con qué nivel de riesgo.

## Bugs a verificar en el workflow WhatsApp

### Bug 1 — tool mismatch "Agendar" / "Reservar"

El system prompt del AI Agent del WhatsApp usa la tool `"Agendar"` entre comillas en los pasos del flujo de agendamiento, pero el nodo real se llama `"Reservar"`. Efecto: cuando un cliente confirma una hora de demo, el agente dice "te reservo el jueves a las X" pero **no ejecuta la tool**, el evento nunca se crea en el calendar.

**Cómo verificar**: buscar en el system prompt del nodo `AI Agent1` las menciones de `Agendar`. Si aparecen y el nodo se sigue llamando `Reservar`, el bug está presente.

**Impacto estimado**: las demos agendadas vía WhatsApp podrían no estar apareciendo en el Google Calendar `Leads Agentesia`. Revisar cruzando con el Sheet `Registro de Leads AGENTESIA` filas con `urgencia = cita_agendada`.

### Bug 2 — Google Sheets con `columns.value: {}` insertando filas vacías

El nodo `Registro Sheets` tiene `mappingMode: "defineBelow"` pero `columns.value: {}` vacío. Efecto: las filas se insertan **en blanco** sin dar error — el agente llama la tool correctamente pero los datos no se mapean.

**Cómo verificar**: abrir el Sheet `Registro de Leads AGENTESIA` (`1kEUGE3q58A0yqIOj6YZKie6EtJmQ8OCDDYahKu27NCk`) y mirar las filas recientes. Si hay filas con columnas vacías (Nombre, Teléfono, etc.) pero con timestamp, el bug está confirmando.

**Impacto estimado**: potencialmente **meses de leads capturados sin datos**. Este es el bug más preocupante.

### Bug 3 — Agente re-dispara tools de escritura en cada turno

`memoryPostgresChat` no persiste tool calls. Sin una regla "no-repeat" en el system prompt, el agente re-llama `Registro Sheets` + `Lead caliente` / `Lead cita DEMO` en cada mensaje nuevo del cliente.

**Cómo verificar**: revisar el historial de Slack del canal `C0ARXC2L406` buscando duplicados del mismo lead. Cruzar con el Sheet buscando filas duplicadas (mismo nombre + teléfono).

**Impacto estimado**: duplicación de leads en Sheets y notificaciones Slack repetidas. Menos crítico que el bug 2 pero molesto para el equipo.

## Fixes aplicables

Los fixes ya están documentados y validados en el workflow Web Chat Agentesia. Ver [[web-chat-workflow]] sección "Bugs encontrados y fixes aplicados" para el patrón exacto de cada fix. Reaplicar los mismos cambios al workflow WhatsApp.

## Riesgo de tocar WhatsApp

- Es producción activa — clientes reales escribiendo al número
- Tiene más lógica que el Web: integración con Chatwoot, Redis sentinel para batches de mensajes, análisis de imágenes, transcripción de audios
- Cualquier error en el PUT de la API puede tumbar el agente de WhatsApp y afectar atención al cliente real

**Estrategia sugerida**:
1. Exportar el workflow WhatsApp a JSON antes de tocar nada (backup)
2. Aplicar los 3 fixes en entorno aislado si es posible, o en una ventana de bajo tráfico
3. Verificar con un mensaje de test tras cada fix antes de pasar al siguiente
4. Monitorizar Slack y Sheets durante las horas siguientes

## Cuándo hacerlo

Decisión pendiente del usuario. No urgente si el WhatsApp está "funcionando" percibidamente, pero urgente si el bug 2 está perdiendo datos de leads silenciosamente desde hace tiempo.

## Actualización 2026-04-16

El workflow de WhatsApp `enVlCyi7McKfwkRQ` ha sido reemplazado por `ChatBOT mejorado` (id `89B9QN23hOHDq6oP`) que usa Chatwoot como hub en vez de conexión directa a Meta. El workflow viejo está **pendiente de desactivación** — ver `inbox/desactivar-workflow-antiguo-chatbot-agentesia.md`. La auditoría de bugs 1-4 debería verificarse en el workflow nuevo si aplica, aunque el nuevo se construyó con los fixes ya aplicados.

## Actualización 2026-04-17 — ARCHIVADO

Esta nota se considera **resuelta**. El ChatBOT mejorado (`89B9QN23hOHDq6oP`) está activo en producción con los fixes aplicados (tool names correctos, Sheets mapping, reglas anti-repeat). Además se ha integrado el sistema de ticketing (tool "Crear Ticket" conectada al portal de clientes). El workflow viejo sigue pendiente de desactivación (ver inbox correspondiente).
