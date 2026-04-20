---
title: facturaia estado y pendientes
date: 2026-04-20
source: claude-code-session
tags: [facturaia, agentesia, proyecto]
---

# FacturaIA — Estado actual (20 abril 2026)

**Repo**: `/Users/manueldelmonte/facturaia` → `AgentesIAMadrid/facturaia`
**Dominio**: `facturaia.agentesia.world` (185.99.186.76, Dokploy)
**Supabase**: proyecto `lahqlyaxvobqjgdiftag` (Cloud, eu-west-1)
**n8n**: workflow OCR `zf2la2N2YBXKQNKk` en `n8n.agentesia.world` (compartido)
**Stack**: Next.js 16 App Router + React 19 + CSS custom + SVG charts custom + Supabase Cloud + OpenAI GPT-4o-mini

## Completado

### Infraestructura
- Schema SQL ejecutado (17 tablas + RLS multi-tenant + funciones SECURITY DEFINER)
- Auth funcional (login/registro + onboarding org)
- Docker compose con env vars hardcodeadas (Dokploy no inyecta `${VAR}`)
- Deploy manual funcional (requiere reload Traefik post-deploy)

### OCR Pipeline
- Upload → Supabase Storage → n8n webhook → OpenAI GPT-4o-mini Vision → Supabase update
- Next.js convierte a base64 (n8n sandbox no puede), envia via webhook
- Prompt incluye `org_nombre` para distinguir proveedor vs cliente
- Progreso simulado en frontend (0→90%) hasta que n8n responde con 100%
- Realtime Supabase para updates instantáneos en la bandeja

### Dashboard principal
- 5 KPIs con sparklines reales (agrupadas por semana), trends calculados vs periodo anterior
- Subtítulos dinámicos (conteo facturas, clientes únicos, mes actual)
- Cashflow chart SVG real (6 meses pasados + 3 previsión IA)
- Donut de estado facturación con datos reales
- Alertas generadas dinámicamente desde datos (vencidas, IVA próximo, pendientes altas, cashflow)
- Próximos vencimientos, top clientes, ingesta automática — todo con datos reales

### Facturas (emitidas + recibidas)
- Tabla con agrupación por mes, totales calculados
- CRUD completo: editar (modal), eliminar (confirmación), cambiar estado
- Filtros funcionales: estado, cliente/proveedor, periodo, IVA%, rango importe
- Exportar CSV
- Bulk actions (marcar cobrada/pagada múltiples)
- Menu contextual con dots

### Ingesta IA (bandeja)
- Lista compacta con realtime
- Preview de documento (imagen o PDF iframe)
- Campos extraídos editables (click-to-edit, Enter/Escape, persistencia Supabase)
- Aprobar → crea proveedor por NIF + inserta factura recibida
- Descartar, eliminar
- Chip de confianza OCR (alto/medio/bajo)

### Otras vistas funcionales
- Cashflow detallado con helper compartido `src/lib/cashflow.ts`
- Clientes/proveedores con facturado/pendiente/gasto calculado real
- Presupuestos con tasa de conversión real
- Calendario, informes IVA, generador PDF — todo con datos Supabase
- Settings: 18 secciones, nueva serie, tipo impuesto, tema, canales, integraciones
- Agentes: toggle activo/inactivo guarda en DB
- Toasts para feedback de todas las acciones

## Pendiente

### Prioridad alta
- **Test end-to-end OCR en producción** — subir factura real desde facturaia.agentesia.world y verificar todo el pipeline
- **Deploy automático** — Dokploy no auto-deploya al push. Investigar webhook GitHub → Dokploy
- **Verificar que n8n no se cae al redesplegar FacturaIA** — comparten servidor y Traefik

### Prioridad media
- **Developer dashboard `/admin`** — panel para activar/desactivar funciones por organización
- **Ingesta multicanal real** — WhatsApp (Chatwoot webhook), Telegram (bot), email (forwarding)
- **Generador PDF mejorado** — enviar por email, guardar como emitida automáticamente

### Futuro
- Agentes IA conectados a n8n (cobros automáticos, clasificador, copiloto IVA)
- Búsqueda global
- Mobile responsive final polish

## Arquitectura OCR

```
[Usuario sube archivo]
    ↓
[Next.js /api/upload]
    → Supabase Storage (bucket 'facturas')
    → Insert bandeja_ingesta (estado: procesando)
    → base64 del archivo + org_nombre
    ↓
[n8n webhook /factura-ocr]
    → Code Node: construye request OpenAI con prompt + org_nombre
    → HTTP Request: POST api.openai.com/v1/chat/completions (gpt-4o-mini)
    → Code Node: parsea JSON de respuesta
    → HTTP Request: PATCH Supabase bandeja_ingesta (estado: listo, datos_extraidos)
    ↓
[Realtime Supabase → Frontend actualiza automáticamente]
```

## Credenciales (referencias)

- Supabase URL/keys: memory `supabase-facturaia.md`
- OpenAI API key: memory `openai-api-key.md`
- n8n API key: memory `n8n-agentesia-world-api.md`
- Anthropic API key: memory `anthropic-api-key.md` (no se usa para OCR — billing separado de Claude Max)
