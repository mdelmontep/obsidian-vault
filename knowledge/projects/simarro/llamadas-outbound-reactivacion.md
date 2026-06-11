---
title: Llamadas outbound de reactivación (Opción C)
date: 2026-06-11
source: implementación Claude Code 2026-06-10/11
tags: [simarro, retell, outbound, kommo, n8n]
---

# Llamadas outbound de reactivación — Simarro

Llamadas IA salientes (Ana) a leads fríos: cada **≥10 días** desde el último intento/actividad, schedule **L-V 10:30** Europe/Madrid (lo vencido en finde se llama el lunes), cap **3 intentos** por lead.

## Legal

- Gate técnico: CF checkbox **Consentimiento outbound `1376604`** — solo se llama si está marcado. De momento se marca **a mano** en Kommo (decisión Manu 2026-06-10). Base: Art. 66.1.a Ley 11/2022 (consentimiento previo expreso).
- **Lista Robinson**: documentada pero NO se usa aún (decisión Manu). Antes de escalar volumen, cruzar los teléfonos contra ella.

## Piezas

| Pieza | ID |
|---|---|
| Agente Retell | `agent_042b9fbc990838ae4117315440` "Ana Outbound (Reactivacion)" — voz custom + **eleven_multilingual_v2, voice_temperature 1.1** (turbo_v2_5 sonaba robótica, cambiado 2026-06-11), responsiveness 0.85, voicemail hangup, max 10 min |
| Conversation Flow | `conversation_flow_29839e6fd152` — **v2 2026-06-11, 17 nodos** (rediseño tras 2ª llamada test); apertura "¿Hablo con {{nombre_lead}}?"; consentimiento con frase cerrada anti-RGPD; tools `Mirar_disponibilidad`/`Reservar`/**`Buscar_viviendas`** = mismos webhooks que el inbound. Camino descubrimiento: proponer vivienda → si no encaja, preguntar qué busca → tool búsqueda en cartera → presentar → reserva. Global prompt: una pregunta por turno, no preguntar+despedirse en mismo turno, "esa no pero sigo buscando" ≠ rechazo, TTS en palabras |
| n8n lanzador | `Llamadas_outbound (reactivacion)` (`2LqwDgLecHwjgIQl`) — cron `30 10 * * 1-5` + `POST /webhook/outbound_run`. **INACTIVO** hasta test real |
| n8n handler | `Retell_outbound_eventos` (`flhsvOskRZiHrcKu`) — **ACTIVO**, webhook `retell_outbound_eventos`, filtra `call_analyzed` del agente outbound |
| BD | `sql/017_outbound_calls.sql` (tabla `outbound_calls` + 3 RPCs SECURITY DEFINER) — **APLICADA 2026-06-11** (Manu, verificada en vivo vía webhook fake → RPC 200 idempotente) |
| Cred n8n Retell | `V67lij4FrDxKqrlQ` (httpHeaderAuth Bearer) |

## CFs Kommo (lead)

`1376604` Consentimiento (checkbox) · `1376606` Intentos (numeric) · `1376608` Último intento (date_time) · `1376610` Resultado (select: 1027074 Visita agendada / 1027076 No interesado / 1027078 Pide más info / 1027080 Derivado humano / 1027082 Sin conversación / 1027084 No contesta).

## Selección (lanzador)

Etapas elegibles: pool Buscando vivienda ×3 embudos (`106971083`/`105358051`/`105358071`) + En seguimiento `107269819` + Post-visita `107269815`. Filtros: consentimiento ✓, intentos <3, ≥10 días desde CF último intento (o `updated_at` si nunca llamado). Contacto principal → teléfono E.164 (+34). Loop 1 a 1, Wait 1.2 s. `POST /v2/create-phone-call` con `metadata {lead_id, attempt, campaign}` (el handler depende de él). Intentos+1 y timestamp SOLO si la llamada se lanzó.

## Handler (acciones por resultado)

- `visita_agendada` → nota + CF. **NO mueve a Lead Caliente**: la tool Reservar ya dispara el circuito estándar (lead nuevo + salesbot 87865); moverlo duplicaría la confirmación WA con "Día de visita" vacío.
- `no_interesado` → Venta Perdido `143` + nota con motivo.
- `pide_mas_info` → nota + tarea Follow-up Ramón +24 h.
- `derivado_humano` → nota + tarea Follow-up Ramón +4 h (sin transfer en caliente: Ana promete callback).
- `no_contesta` / `sin_conversacion` → nota + CF, reintento a los 10 días.
- `no_contactar` → desmarca consentimiento `1376604`.
- Idempotencia del webhook duplicado: RPC `outbound_record_result` (requiere 017 aplicada; mientras tanto los RPC nodes fallan en silencio con `onError: continue`).

## Go-live

1. ~~Aplicar `sql/017`~~ — hecho 2026-06-11.
2. Test llamada real — 2 llamadas hechas (52s y 92s): handler E2E OK, análisis post-call correcto; feedback voz → multilingual_v2; transcripción incoherente → flow rediseñado v2 (17 nodos + tool búsqueda). **Falta 3ª llamada validando el flow nuevo.**
3. Marcar consentimiento en leads autorizados por Ramón.
4. Activar `2LqwDgLecHwjgIQl`.

Relacionado: [[estado-actual]], [[routing-citas-por-agente]].
