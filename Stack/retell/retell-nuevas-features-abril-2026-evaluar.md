---
title: retell nuevas features abril 2026 — evaluar e implementar
date: 2026-04-18
source: retell-newsletter
tags: [retell, voice, roadmap]
---

# Retell — Nuevas features abril 2026

## Implementar pronto (alto impacto)

### JavaScript en conversation flow
Ejecutar JS directamente en el flujo sin pasar por n8n.
- Extraer nombre de pila del contacto para saludo natural
- Formatear fechas/horas al español ("martes 22 a las 4 de la tarde")
- Validar formato de teléfono o DNI antes de guardar en CRM
- Lógica de reintentos (máximo 3 intentos antes de escalar)
- **Beneficio**: menos latencia al eliminar round-trips HTTP a n8n para operaciones simples
- Docs: https://docs.retellai.com (buscar "JavaScript node")

### Subagent Nodes
Dividir agentes monolíticos en subagentes especializados con transiciones.
- Subagente "recepción" → saluda, identifica motivo
- Subagente "citas" → conversa + consulta disponibilidad + agenda
- Subagente "transfer" → pasa a humano si urgencia
- **Beneficio**: prompts más cortos, debug más fácil, cada subagente con sus tools
- Probar primero con Clinica Zen
- Docs: https://docs.retellai.com (buscar "Subagent")

### SMS en llamada
Enviar SMS durante la llamada activa.
- Confirmación de cita al paciente en el momento
- Enviar links (formularios previos, ubicación clínica)
- Funciona con número Retell SMS-approved o número propio
- **Caso clínicas**: "Tu cita: martes 22 abril, 16:00, Dr. García" enviado durante la llamada
- Docs: https://docs.retellai.com (buscar "In-Call SMS")

## Implementar después (útil pero no urgente)

### Agent Timezone Settings
- Configurar `Europe/Madrid` por agente
- Elimina hardcodeo de timezone en prompts

### Audio Testing desde nodo específico
- Debug sin pasar por el flujo completo cada vez
- Arrancar test desde el nodo de citas directamente

### Custom Post-Call Analysis para alertas
- Detectar llamadas con quejas o fallos del agente
- Enviar alerta a Slack automáticamente
- Sustituiría parte de la lógica post-call que ahora pasa por n8n

## Ignorar por ahora

- **Agent Handbooks** — ya tenemos prompts propios con anti-hallucination, los presets genéricos aportan poco
- **Transfer Language Controls** — solo trabajamos en español
- **Conversation Flow Notes** — documentación interna, nice-to-have
