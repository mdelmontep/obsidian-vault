---
title: top of mind
date: 2026-04-20
tags: [home, prioridades]
---

# Top of Mind

## Prioridades esta semana

- **FacturaIA — sesión larga de mejoras en curso** — calendario interactivo, cashflow con negativos, pills con pulso, filtros por rango de fechas, settings de apariencia (colores, tipografía Mermaid, pills, categorías), smart alerts, top proveedores, previsión de gastos fijos. Seed con 60 facturas realistas + PDFs generados con pdf-lib.
  - **PENDIENTE INMEDIATO**: verificar visualmente en navegador que las facturas emitidas muestran nombres de clientes (datos OK en BD, falta hard refresh), verificar recibidas distribuidas correctamente entre proveedores, probar click en número de factura para previsualizar PDF, verificar columnas no se cortan
  - **PENDIENTE**: deploy a producción (push + Dokploy redeploy + Traefik reload), test e2e OCR en prod
- ~~Mover repos de AgentesIAMadrid a cuenta personal GitHub~~ PARCIAL — `obsidian-vault` movido a `mdelmontep/obsidian-vault` (privado)
- **Clinica Zen — pendientes post-migración**:
  - Cambiar Google Calendar ID en TODOS los workflows
  - Cancelación de cita debe borrar evento del calendario (no implementado)
  - Verificar contenido RAG actualizado para CZ
- **Clinica Zen: Chatbot prompt v7 aplicado — pendiente test real WhatsApp**
- **Clinica Zen: Test cancelar/cambiar cita** — flujo completo sin probar
- Notificaciones de tickets del dashboard a Slack `#01-tickets-soporte`
- Repo GitHub privado para skill chatbot-chatwoot-replicator

## Bloqueos activos

- Clinica Zen: pendiente scope "Chats" de Kommo (contactar soporte)

## Completado reciente

- FacturaIA: 60 facturas seed (40 emitidas, 20 recibidas) con distribución round-robin de clientes/proveedores
- FacturaIA: 60 PDFs profesionales generados con pdf-lib y subidos a Supabase Storage
- FacturaIA: calendario interactivo con filtros, approve de sin_aprobar, click para navegar a factura
- FacturaIA: filtro por rango de fechas con 7 presets (esta semana, mes, trimestre, año, anteriores)
- FacturaIA: pills con pulso (rojo vencidas/cerca vencimiento, verde cerca cobro)
- FacturaIA: cashflow chart arreglado para valores negativos
- FacturaIA: settings apariencia funcional (brand colors, tipografía incluyendo Mermaid, pill colors, categorías)
- FacturaIA: panel previsión gastos fijos en dashboard (6 gastos recurrentes seeded)
- FacturaIA: top proveedores y smart alerts (5 tipos) en dashboard
- FacturaIA: número de factura clickeable para previsualizar PDF en modal
- FacturaIA: tabla facturas con layout fijo para evitar columnas cortadas
- FacturaIA: proveedores 3-dot menu arreglado con createPortal
- FacturaIA: donut chart "Estado de facturación" arreglado (faltaba estado enviada)
- FacturaIA: fuente Mermaid añadida como opción de tipografía
- Agente de voz Retell CZ creado via API
- Chatbot CZ prompt v7 completado
- FacturaIA Fases 1-5 completadas
