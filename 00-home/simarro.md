---
title: simarro
date: 2026-05-07
tags: [cliente, simarro]
---

# Simarro Properties

Inmobiliaria. Chatbot WhatsApp + agente de voz Retell + Kommo CRM + scraping inmuebles. Contacto: Ramón.

## Estado

- **Chatbot WhatsApp** activo (~2s respuesta tras fix Wait node 2026-05-04). Workflow n8n `zYcHHa8jWXB6dY5i` rama Simarro
- **Agente voz Retell** Ana — llama a `+34 919 93 28 52`. Tool `Buscar_viviendas` operativa
- **Kommo CRM** integrado, salesbots de recordatorio (4h y 24h) funcionando
- **Web** en simarro_web (Vercel), webhook seguro con `N8N_WEBHOOK_TOKEN`

## Próximos hitos

1. **Preguntar a Ramón** (NEXT) — flow citas (bot reserva o fecha provisional) + pipeline Kommo actual
2. **Verificar salesbot 88183** (NEXT) — acción "Enviar WhatsApp" con `{{lead.cf.1372573}}` en editor Kommo
3. **IDs TODO en n8n** (LATER) — TASK_TYPE_ID, RESPONSIBLE_USER_ID, SHEET_ID_LEADS_WEB
4. **Monitor inmuebles tipo StateFox** (LATER) — Apify igolaizola + n8n + Kommo. Confirmar interés y presupuesto

## Bloqueos / esperando a terceros

- Ramón: re-autorizar credencial GCal `d3uDK7X9ZflAoumq` (estaba en Forbidden, verificar si sigue)

## Links rápidos

- n8n: workflow Simarro `zYcHHa8jWXB6dY5i` rama
- Kommo dashboard: agentesialab.kommo.com
- Retell agent: `+34 919 93 28 52`
- WhatsApp test: enviar a `+34 919 93 28 52`

## Histórico de hitos

- 2026-05-04: chatbot lentitud arreglada (Wait node + Redis restaurado)
- 2026-05-04: salesbots Recordatorios funcionando (87861=4h, 87871=24h)
