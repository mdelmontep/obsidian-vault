---
title: tool description generica no fuerza ejecucion de tool critica
date: 2026-04-19
source: claude-code-session
tags: [n8n, ai-agent, tool-calling, bug]
---

El nodo `Reservar_cita` (toolWorkflow) tenía una descripción de 74 caracteres: "Usa esta herramienta para reservar cita, una vez confirmada por el usuario". El LLM (GPT-5.1) generó texto de confirmación ("Te reservo a las 11:00") **sin ejecutar la tool**. La cita nunca se registró.

## Fix

Expandir la descripción a ~280 chars explicando las **consecuencias de no llamar**:

> "OBLIGATORIO para registrar una cita. Usa esta herramienta SIEMPRE que el paciente confirme la reserva. Sin ejecutar esta herramienta, la cita NO queda registrada en el sistema aunque hayas escrito un mensaje de confirmación. Necesita: nombre, teléfono, email, servicio, fecha y hora."

Además, reforzar en el system prompt:
- Regla crítica #1: "SIEMPRE ejecuta Reservar_cita cuando el paciente confirme"
- En el paso de reserva: "OBLIGATORIO. SIN ESTA LLAMADA LA CITA NO EXISTE"
- En el paso post-reserva: "Solo DESPUÉS de que Reservar_cita se ejecute con éxito"

## Patrón general

Para toda tool que realice una **acción de escritura irreversible** (reservar, cancelar, enviar email, crear registro), la descripción debe:
1. Decir que es OBLIGATORIA en el contexto correspondiente
2. Explicar qué pasa si NO se llama (la acción no ocurre)
3. Listar los parámetros requeridos

Una descripción genérica de una línea no es suficiente — el LLM la trata como opcional.

## Complemento (2026-05-03)

Si la description ya es agresiva pero el agente sigue fabulando (ej. inventa slots de calendario sin llamar `Mirar_disponibilidad`): bajar `temperature` a `0`. Síntoma diagnóstico: ejecución con `intermediateSteps=0` cuando debería haber al menos 1 tool call.
