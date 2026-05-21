---
title: Retell voice agent inbound castellano — config canónica
date: 2026-05-10
source: sesión Simarro Properties (Ana) — afinado producción
tags: [retell, voice, inmobiliaria, latencia, castellano]
---

Config validada en producción para **voice agent inbound en español castellano** tras varias rondas de afinado contra patinazos. Aplicar como baseline al replicar.

## Voice config (Retell agent)

| Param | Valor | Por qué |
|---|---|---|
| `voice_speed` | **1.0** | >1.05 con voz clonada (Cartesia/ElevenLabs) introduce artefactos perceptibles como stutter. |
| `voice_temperature` | **0.5** | 0.6+ en custom voice = más variabilidad → tropiezos. 0.4-0.5 estable. |
| `interruption_sensitivity` | **0.5** | 0.7+ hacía que Ana cortara con cualquier ruido del cliente (respiración, "ehm"). 0.5 = sweet spot defensivo. |
| `responsiveness` | **0.7** | Con sonnet-4.6 (TTFT alto), 0.6 daba arranques antes de tener buffer → micro-pausas. 0.7 espera lo justo. |
| `ambient_sound` | **null** | Tener call-center a vol >1.0 + denoising agresivo creaba "pumping" perceptible como stutter. |
| `denoising_mode` | **noise-cancellation** | "noise-and-background-speech-cancellation" es demasiado agresivo, come parte del audio. |
| `handbook_config.speech_normalization` | **true** | Sin esto, números/fechas/CP causan re-chunking del TTS mid-stream — causa #1 del patinazo. Equivalente a `normalize_for_speech: true`. |
| `enable_dynamic_responsiveness` | **false** | True con muletillas castellanas ("eh", "pues") clasifica mal turn-taking → cortes raros. |
| `begin_message_delay_ms` | **1000** | 0 patinaba el saludo (audio path WebRTC no listo). 500 funciona casi siempre. 1000 = totalmente seguro. |
| `voicemail_detection_enabled` | **false** | Solo aplica outbound. Inbound = irrelevante; falsos positivos con mayores. |
| `tool_call_strict_mode` | **false** | Permite omitir args opcionales (ej. `idealista_id` vacío en visita genérica). |
| `start_speaker` | **agent** | Ana saluda primero, no espera al cliente. |

## Voice provider

**ElevenLabs Flash v2.5** > Cartesia-Isabel para castellano:
- TTFB ~75ms vs ~90ms.
- Voz natural, sin artefactos a 1.0× speed.
- Mejor pronunciación de palabras boost-keywordeadas.

Si replicas, probar Flash v2.5 antes que Cartesia.

## Caller ID via `{{from_number}}`

Variable estándar Retell para inbound. Disponible en system prompt directamente:

```
Tu sistema tiene el Caller ID en {{from_number}}. Léelo SIEMPRE al cliente
en grupos de tres en UN SOLO TURNO: "el [trío] - [trío] - [trío], ¿verdad?".
SIN frases de relleno tipo "déjame confirmar".
Si {{from_number}} viene vacío o el cliente dice no es correcto, pídele el
bueno y léelo en grupos de tres.
```

UN solo turno: leer + preguntar. Sin "voy a verificar tu teléfono… déjame confirmarlo… espera…" — Ana se queda en bucle.

## Tool timeouts canónicos (NO defaults Retell de 60-120s)

```json
{
  "Mirar_disponibilidad": 3000,
  "Buscar_viviendas": 4000,
  "Buscar_reserva": 4000,
  "Reservar": 6000,
  "Cancelar_cita": 6000,
  "Derivar_agente": 4000
}
```

Si una tool timeout-ea, el LLM ve el error y puede recuperar gracefully. Default 60s = silencio inaceptable.

## Filler ultra-corto en `execution_message_description`

| Tool | Filler |
|---|---|
| `Reservar` | `"Te apunto."` |
| `Buscar_reserva` | `"Mirando."` |
| `Mirar_disponibilidad` | `"Mirando agenda."` |
| `Buscar_viviendas` | `"A ver."` |
| `Cancelar_cita` | `"Un segundo."` |

Filler 250-700ms cubre p50 de la tool. Filler largo (>1.2s) sobre-rellena cuando la tool tarda menos → robotizado. Filler corto + silencio post (<300ms) es preferible a sobre-relleno.

## Test playground markers

Retell test playground (web simulation):
- `call_id == "playground"`
- `call_type == "web_call"`

Producción inbound:
- `call_id == "call_<uuid>"`
- `call_type == "phone_call"` o `"inbound_phone_call"`

Usar `call_type=web_call` como GUARD en n8n para skipear acciones reales (Send WhatsApp, polling de call status, inserts a Postgres analytics) durante tests.

## `confirmation_text` formateado en n8n, no LLM

Bug repetido: el LLM (incluso sonnet-4.6 temp 0.18) falla formateando fechas con timezone y direcciones largas → dice "tres y media" cuando es "una y media", o repite municipio.

**Patrón obligatorio**:
1. n8n compone el `confirmation_text` con código JS determinista (helpers `hourWord/timeToWords/dayPart/numberToWords/weekdayName/splitAddress`).
2. Devuelve campo `confirmation_text` en la response.
3. System prompt fuerza:
   > *"Tras Reservar, lee LITERAL el campo `confirmation_text` palabra por palabra. PROHIBIDO reformular dirección, fecha, hora ni añadir frases extra."*

Aplicable a cualquier tool que devuelva confirmación factual al cliente.

## Modelo LLM

**claude-4.6-sonnet** temp 0.18 funciona bien con prompt ~3000 tokens. TTFT ~380-450ms.

Alternativa: `claude-sonnet-4` standard tiene TTFT ~320ms (-80ms) pero pierde inteligencia notable en máquina de estados largas. Para flows con 5+ estados condicionales, mantener 4.6.

## Compresión de prompt

System prompt 4875 tokens prosa-markdown → **3035 tokens XML semántico** mantiene todas las reglas críticas. Reducción 38%.

Estructura ganadora:

```xml
<identity/>
<mission/>
<style/>
<turn_rules/>
<inferences/>
<state_machine/>
<tools_gating/>
<critical_rules/>  ← al final, recency bias
<faq_quick/>
<objections/>
<edge_cases/>
```

Por qué XML > headers markdown para sonnet 4.6: el modelo respeta mejor bloques XML semánticos como reglas duras. `<critical_rules>` al final aprovecha recency bias.

**Sub-2200 tokens** se evaporan reglas condicionales largas (segunda oportunidad ante discrepancia, gating horario transfer/Derivar exclusivo, lectura literal). Mantener `<critical_rules>` al final como red de seguridad.

## Begin message — STATIC, no dynamic

Inbound voice: `begin_message` estático ahorra +1s vs dynamic (no invoca LLM).

```
"Hola, Simarro Properties. ¿En qué puedo ayudarte?"   (~3s TTS)
```

Mejor que *"Buenos días, soy Ana de Simarro Properties..."* (5s, ambiguo en tarde/noche).

Dynamic solo si necesitas:
- Saludo personalizado por nombre (lookup CRM via `call_inbound` webhook → `dynamic_variables`)
- Bienvenida adaptada a hora estricta

## Síntomas → causas (tabla de triage)

| Síntoma | Causa probable | Fix |
|---|---|---|
| Patina al saludo | `begin_message_delay_ms: 0` | Subir a 500-1000ms |
| Patina mid-conversation | speech_normalization off + números en frase | Activar `speech_normalization` |
| Pausa larga antes de hablar | `responsiveness` muy bajo o LLM TTFT alto | Subir responsiveness a 0.7, considerar prompt más corto |
| Corta al cliente cuando duda | `interruption_sensitivity` alto | Bajar a 0.4-0.5 |
| Tartamudea palabras / artefactos | voice_speed >1.05 con voz clonada | Bajar a 1.0 |
| "Pumping" rítmico | ambient_sound + denoising agresivo | ambient null, denoising "noise-cancellation" |
| Bucles repetidos en confirmación de teléfono | falta `{{from_number}}` o prompt no canalizado | usar variable + UN solo turno |

## Anti-patrones detectados

- Filler largo "Un momento, que miro el calendario un momento" cubriendo tool de 600ms → sobre-relleno robotizado.
- Tool timeout default 60-120s en producción → si webhook cuelga, Ana queda muda 60s.
- `voicemail_detection_enabled: true` en inbound → falsos positivos con mayores que tardan en saludar.
- `enable_dynamic_responsiveness: true` para castellano → muletillas confunden al detector.
- LLM componiendo fecha/dirección/ID en respuesta TTS → alucinaciones impredecibles.

## Flex vs Rigid Mode — coste por minuto

Conversation Flow tiene 2 modos compilación. Flex compila TODO (nodos + edges + KB + tools) en UN prompt enorme. Si supera 3.500 tokens → Retell aplica **token-scaling multiplier x2-5** sobre el LLM. Rigid sólo manda el nodo activo + global_prompt.

| Config | Coste/min castellano |
|---|---|
| Flex + gpt-4.1 cascading high_priority + KB | €0.20-0.35 |
| Flex + gpt-4.1 sin high_priority | €0.18-0.28 |
| **Rigid + gpt-4.1 cascading SIN high_priority** | **€0.135** ← sweet spot |
| Rigid + gpt-4o-mini todo | €0.115 (perdida calidad voice) |

**Regla**: por defecto Rigid. Flex solo si necesitas context-switching real entre tareas Y has medido token count en simulator Retell (<3.000 para tener margen).

Ver [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
