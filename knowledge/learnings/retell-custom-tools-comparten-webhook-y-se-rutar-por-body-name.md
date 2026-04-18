---
title: retell custom tools comparten webhook y se rutar por body name
date: 2026-04-18
source: claude-code-session
tags: [retell, n8n, workflow]
---

Todas las custom tools de un agente Retell pueden apuntar al mismo webhook (ej: `/webhook/Reservas`). Retell envía un POST con:

```json
{
  "name": "Crear_ticket",
  "args": {
    "subject": "Chatbot no responde",
    "description": "...",
    "priority": "high",
    "category": "bug",
    "telefono": "617314938",
    "nombre": "Juan Pérez"
  }
}
```

## Ruteo en n8n

1. Nodo Set `Normalizar Datos` extrae `accion` de `$json.body.name`
2. Switch rutar por `accion` → Reservar / Mirar_disponibilidad / Solicitar_callback / Crear_ticket
3. Cada rama procesa sus `args` específicos

## Importante

- `parameter_type: "json"` en la tool de Retell para que los args lleguen como objeto, no como form-encoded
- Si la tool tiene `speak_during_execution: true`, Retell habla mientras espera la respuesta del webhook
- Los args los rellena el LLM del agente según las `parameters.properties` definidas en la tool
