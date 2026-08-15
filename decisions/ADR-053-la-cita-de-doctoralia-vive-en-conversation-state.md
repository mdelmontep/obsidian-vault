---
title: ADR-053 — la cita de Doctoralia se persiste en conversation_state, no en tabla propia
date: 2026-08-15
status: accepted
tags: [adr, elphis, n8n, postgres]
---

## Contexto
El bot de Elphis no podía confirmar una cita ("no puedo acceder a la información de las reservas") porque `doctoralia-email-sync` extraía `fecha_cita_iso` pero solo lo escribía en Clientify y en `idempotency_log`. Constraint duro: sin SSH al host (puertos 22/5251/5432 cerrados desde fuera) **no hay forma de ejecutar DDL** — crear una tabla exigiría un workflow n8n solo para eso.

## Opciones consideradas
- **A — tabla dedicada `cita_agendada`** (status enum, `last_error`): la correcta por el principio de "integración crítica no va en JSONB", pero requiere DDL que ahora mismo no se puede ejecutar.
- **B — leer `idempotency_log.response`** bajo demanda desde `chatwoot-event`: cero escrituras nuevas, pero consulta JSONB sin índice en cada turno y depende de que `response` conserve el shape del extractor.
- **C — `conversation_state.paciente_data.cita`** (JSONB ya existente, que el router ya carga): coste de lectura cero, pero obliga a que el upsert deje de sobrescribir `paciente_data`.

## Decisión
**C**, porque `conversation_state` es exactamente la tabla que modela el estado de la conversación y `paciente_data` ya guarda nombre/motivo/relación del paciente: la cita es un dato más de esa ficha, no el estado de una integración con sus errores. Se cambió `Upsert conv_state` a merge jsonb (`COALESCE(paciente_data,'{}') || EXCLUDED.paciente_data`) para que un turno del bot no borre lo que escribió el sync.

## Consecuencias
No hay `status` ni `last_error` de la sincronización: si el UPDATE no casa por teléfono, se pierde en silencio y solo se ve porque el bot dice "no me consta". Si algún día hace falta observabilidad de esa sincronización (o citas de gente que nunca escribió por WhatsApp, hoy fuera de alcance), esto se migra a **A** — el JSONB es el compromiso por no poder hacer DDL, no el destino. Ver [[el-estado-derivado-tambien-hay-que-sincronizarlo-en-la-rama-que-descarta]] · [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]]
