---
title: guía de prompt engineering para agentes de voz retell
date: 2026-04-23
source: sesión claude code — optimización agente tecnocloud
tags: [retell, voice, prompt-engineering, best-practices]
---

# Guía de Prompt Engineering — Agentes de Voz Retell

Framework para crear prompts profesionales de agentes de voz. Basado en las best practices de Retell y validado con llamadas reales.

---

## Principio 1: Prompt corto = menos latencia

Cada token en el prompt suma latencia en cada turno. Target de respuesta LLM: < 900ms.

- Lo que se pueda resolver por config del agente, NO va en el prompt
- Eliminar redundancia: cada regla aparece UNA vez
- No repetir en "reglas" lo que ya dice el "flujo"

## Principio 2: Estructura seccional obligatoria

El LLM procesa mejor secciones con `##` que bloques de texto. Estructura recomendada:

```
## Identidad        → quién es, empresa, contexto, variables dinámicas
## Estilo           → personalidad, tono, calibración de empatía
## Reglas de respuesta → límites por turno, fluidez, concisión
## Pronunciación    → solo lo que NO cubre config (URLs, rutas, teclas)
## Estados          → máquina de estados con transiciones
## Instrucciones de herramientas → cada tool anclada a un estado
## Casos especiales → excepciones al flujo normal
```

## Principio 3: Usar config del agente antes que prompt

### pronunciation_dictionary (PATCH /update-agent)
Palabras que el TTS debe pronunciar de forma específica. Va en la config del agente, NO en el prompt. Formato:

```json
{"word": "Gmail", "alphabet": "ipa", "phoneme": "yimail"}
```

Cada palabra que metas aquí ahorra tokens del prompt.

### handbook_config
- `speech_normalization: true` — formatea números, fechas, dinero automáticamente
- Los presets de Handbook (High Empathy, Echo Verification, etc.) son genéricos en inglés. Para agentes en español con personalidad definida, mejor controlarlo desde el prompt.

### boosted_keywords
Lista de palabras clave para mejorar la transcripción (nombres de empresa, apps, términos técnicos). Va en config del agente.

### Otros parámetros de agente
- `responsiveness`: 0.6-0.8 (balance entre cortar y esperar)
- `enable_dynamic_responsiveness`: true
- `stt_mode`: "fast" para menos latencia
- `voice_temperature`: ~0.7 para variación natural
- `voice_speed`: ~1.0-1.05
- `ambient_sound`: según contexto ("call-center", "off", etc.)

## Principio 4: Estados mentales en vez de pasos lineales

Los pasos lineales (1, 2, 3...) fallan cuando la conversación no sigue orden. Los estados son más robustos: el agente siempre sabe en qué estado está y qué puede/no puede hacer.

### Estructura de un estado
```
### Estado: NOMBRE
Objetivo: una frase.
- Qué hacer en este estado (reglas positivas).
- Herramientas permitidas o prohibidas.
- Transición → OTRO_ESTADO cuando [condición].
```

### Estados típicos de soporte
```
IDENTIFICANDO  → saber qué pasa y quién llama
DIAGNOSTICANDO → buscar solución (tool de consulta)
GUIANDO        → dar solución paso a paso (sin tools)
ESCALANDO      → derivar al equipo humano
CERRANDO       → verificar, registrar y despedir
```

### Transiciones
- IDENTIFICANDO → DIAGNOSTICANDO: cuando tienes problema + datos del cliente
- DIAGNOSTICANDO → GUIANDO: si la FAQ devuelve solución válida
- DIAGNOSTICANDO → ESCALANDO: si la FAQ no aplica
- GUIANDO → CERRANDO: si el cliente confirma que funciona
- GUIANDO → ESCALANDO: si no funciona tras todos los pasos
- ESCALANDO → CERRANDO: tras confirmar teléfono y avisar al equipo
- CERRANDO → cualquier estado: si el cliente pide algo más

## Principio 5: Anclar herramientas a estados

Cada herramienta se ejecuta ÚNICAMENTE en un estado concreto. Esto previene el error más grave: llamar tools fuera de contexto (ej: registrar llamada a mitad de una guía técnica).

```
### tool_consulta
- Ejecutar ÚNICAMENTE en estado DIAGNOSTICANDO.
- Trigger: toda consulta técnica.
- execution_message: frase corta de espera.

### tool_registro
- Ejecutar ÚNICAMENTE en estado CERRANDO, después de confirmar que no necesita más.
- Requisitos previos: solución/escalado completado + "algo más" preguntado + teléfono confirmado.
- execution_message: frase corta (NUNCA la despedida).

### end_call
- ÚNICAMENTE en estado CERRANDO, después de tool_registro y despedida.
- Después de end_call, no reabrir conversación.
```

## Principio 6: Reglas positivas > reglas negativas

Los LLMs siguen mejor "haz X únicamente cuando Y" que "NUNCA hagas X". Reformular:

| Negativa (peor) | Positiva (mejor) |
|---|---|
| NUNCA llames registrar antes del cierre | registrar se ejecuta ÚNICAMENTE en CERRANDO |
| NUNCA inventes pasos | toda solución viene de buscar_FAQ |
| NUNCA termines sin pregunta | todo turno termina con pregunta |
| NO llames herramientas mientras guías | en GUIANDO, herramientas prohibidas. Solo habla |

## Principio 7: Empatía calibrada al tono del cliente

El error más común: reaccionar con empatía fuerte ("Uf, qué rabia") ante un cliente que está tranquilo. La regla:

```
Calibra empatía al tono del cliente:
- Tono neutro → responde profesional ("Vale, vamos a mirarlo")
- Frustración real → reconócela ("Vaya, qué faena")
- Alivio → compártelo ("Genial, me alegro")
```

## Principio 8: Fluidez conversacional

El segundo error más común: el agente informa algo y se queda callado sin dar pie a responder.

```
Todo turno DEBE terminar con pregunta o invitación a responder.
Si informas (escalado, registro, espera), cierra preguntando.
```

## Principio 9: Un turno = una acción

```
Cada turno = UNA acción: pregunta, instrucción o confirmación. Máximo 2-3 frases.
Si la solución tiene 4 pasos, son 4 turnos.
Si empiezas una instrucción, termínala completa + pregunta de comprobación.
```

## Principio 10: Validación post-consulta

Cuando una tool devuelve información, verificar antes de dársela al cliente:
1. ¿Coincide la app/tema?
2. ¿Coincide el problema?
3. ¿Los pasos son lógicos?

Si falla cualquiera → descartar y escalar. Inventar o improvisar está prohibido.

---

## Plantilla de prompt

```markdown
## Identidad
Eres [nombre], [rol] de [empresa]. [Personalidad en 1-2 frases]. Frases cortas, ritmo natural. No saludes — ya hay saludo predefinido.

Hora: {{current_time_[timezone]}}
[Datos de contexto: portales, contacto, lista de productos/servicios válidos]

## Estilo
Calibra empatía al tono del cliente. Neutro → profesional. Frustración → reconócela. Alivio → compártelo.
Muletillas naturales con moderación: [ejemplos].
Si no sabes algo, dilo con naturalidad.
Registro correcto: [ejemplos de frases naturales]
Prohibido: [ejemplos de frases corporativas artificiales]

## Reglas de respuesta
1. Un turno = UNA acción. Máximo 2-3 frases. Después PARA.
2. Todo turno termina con pregunta que invite a responder.
3. Si empiezas una instrucción, termínala completa + pregunta de comprobación.
4. Concisión: no repitas lo que el cliente dijo, no parafrasees, no expliques lo no pedido.
5. Ante ambigüedad, pregunta antes de asumir.

## Pronunciación
[Solo lo que no cubra pronunciation_dictionary ni speech_normalization]
URLs: primero nombre natural. Solo deletrea si lo piden.
Teléfonos: agrupados de tres con pausas ( - ).
Los espacios alrededor del guión son obligatorios.

## Estados de la conversación

### Estado: IDENTIFICANDO
Objetivo: saber qué pasa y quién llama.
- [Reglas de identificación]
- Transición → DIAGNOSTICANDO cuando tengas: [requisitos].

### Estado: DIAGNOSTICANDO
Objetivo: buscar solución.
- Ejecuta [tool_consulta].
- Valida resultado (app + problema + lógica).
- Si pasa → GUIANDO. Si falla → ESCALANDO.

### Estado: GUIANDO
Objetivo: dar solución paso a paso.
- Un paso por turno + pregunta de comprobación.
- Herramientas PROHIBIDAS en este estado.
- Si funciona → CERRANDO. Si no → ESCALANDO.

### Estado: ESCALANDO
Objetivo: derivar al equipo.
- Confirma teléfono de contacto.
- Informa que el equipo contactará + pregunta si necesita algo más.
- Transición → CERRANDO.

### Estado: CERRANDO
Objetivo: registrar y despedir. ORDEN ESTRICTO:
1. "¿Algo más?" → espera.
2. Confirmar teléfono si no se hizo.
3. Ejecuta [tool_registro].
4. Despedida → end_call. No reabrir después.

## Instrucciones de herramientas

### [tool_consulta]
- ÚNICAMENTE en estado DIAGNOSTICANDO.
- execution_message: "[frase corta de espera]"

### [tool_registro]
- ÚNICAMENTE en estado CERRANDO, paso 3.
- Requisitos: solución/escalado + "algo más" + teléfono confirmado.
- execution_message: "[frase corta]" (nunca la despedida).
- Campos: [listar campos obligatorios]

### end_call
- ÚNICAMENTE en CERRANDO, paso 4, después de registro y despedida.

## Casos especiales
- [Caso 1]: [qué hacer]
- [Caso 2]: [qué hacer]
```

---

## Checklist antes de publicar

- [ ] pronunciation_dictionary actualizado en config del agente
- [ ] boosted_keywords con nombres de empresa/apps/términos técnicos
- [ ] speech_normalization activado en handbook
- [ ] Prompt sin diccionario fonético (ya está en config)
- [ ] Prompt sin reglas redundantes (cada regla aparece 1 vez)
- [ ] Cada herramienta anclada a exactamente 1 estado
- [ ] Todas las transiciones de estado definidas
- [ ] Todos los turnos del agente terminan con pregunta
- [ ] Reglas formuladas en positivo ("únicamente en X" vs "nunca fuera de X")
- [ ] Empatía calibrada al tono, no automática
- [ ] Testar con 3-5 llamadas de prueba cubriendo: flujo feliz, escalado, caso especial
