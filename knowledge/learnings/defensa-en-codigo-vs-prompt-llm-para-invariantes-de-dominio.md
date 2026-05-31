---
title: defensa en código contra LLM creativo para invariantes de dominio
date: 2026-05-21
source: claude-code-session
tags: [llm, n8n, prompt, defensa, dominio]
---

El system prompt es soft: el LLM puede ignorar reglas explícitas, sobre todo cuando los datos parecen "casi completos". Si la regla es un invariante de dominio (precio>0, NIF obligatorio en factura, factura no nace anulada), validar en code node downstream.

Patrón: agente devuelve JSON estructurado → code node intermedio inspecciona campos críticos → si falla invariante, transforma respuesta en `{error:true, conversacional:true, message:"pregunta concreta"}` y reusa el reply de texto plano. El user nunca ve el resumen malo.

Casos reales 2026-05-21 TuFacturaIA bot:
- Precio 0€ aunque prompt decía "NUNCA inventes precio" → guard `precio_unitario <= 0 && !desde_catalogo`.
- Factura sin NIF aunque prompt lo exigía → guard `tipo=='factura' && !cli.nif && !cli.id`.

Variante "pre-computar y ofrecer lista cerrada": si el LLM debe ELEGIR entre opciones derivables por código, no le pidas calcularlas en prosa — el backend devuelve la lista válida y el LLM solo elige. Caso Simarro 2026-05-31: `Mirar_disponibilidad` devolvía texto ("bloqueado 11:30-13:30, resto libre") y gpt-4.1-mini no descontaba la visita de 1h → ofrecía horas que invadían el margen. Fix: el webhook devuelve `slots:["10:00","13:00"]` ya filtrados; prompt = "ofrece slots[0]/slots[1], NO calcules".

Aplica también a: validación algorítmica (NIF, IBAN), business rules (estado válido), límites (cantidad>0). Ver [[n8n-set-node-output-solo-lleva-assignments-explicitos]].
