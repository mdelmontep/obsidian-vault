---
title: copiloto — campo zod requerido impide llamada al tool, llm pide en texto
date: 2026-06-28
source: claude-code-session
tags: [copiloto, whatsapp, llm, zod, tool-use]
---

**Problema**: campo requerido en Zod (`z.string().min(1)`) → el LLM no puede
llamar el tool sin ese valor → lo pide en texto libre. Ningún prompt fix ayuda:
el schema gana.

**Segundo problema**: confirmación del tool A cortaba el turno; el handler
retornaba sin relanzar el modelo para el tool B (el usuario necesitaba dos
confirmaciones separadas en flujos compuestos).

**Fix — compound tool con campo optional + preview gate**:
1. Campo faltante = `z.string().optional()` en el schema.
2. `preview()` lanza `Error("Dame el NIF de «X»")` si falta.
3. Gate `blocked` → history persiste `tool_result(is_error)` → LLM reintenta
   en el siguiente turno con el dato que dio el usuario.
4. Una sola confirmación cubre ambas operaciones (cliente + factura).

**Patrón aplicado**: `crearClienteYFacturar` (v20, #575, G5·A S2).
Aplica a cualquier tool WhatsApp donde el usuario proporciona el dato a posteriori.
