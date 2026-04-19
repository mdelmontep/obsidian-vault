---
title: facturaia estado y pendientes
date: 2026-04-19
source: claude-code-session
tags: [facturaia, agentesia, proyecto]
---

# FacturaIA — Estado actual

**Repo**: `/Users/manueldelmonte/facturaia`
**Dominio**: `facturaia.agentesia.world` (185.99.186.76)
**Supabase**: proyecto `lahqlyaxvobqjgdiftag`
**Stack**: Next.js 15 App Router + React 19 + CSS custom + SVG charts custom + Supabase Cloud

## Completado

- Fase 0: Scaffold + CSS del prototipo + types + Docker config
- Fase 1: 12 vistas completas (dashboard KPIs, facturas emitidas/recibidas, ingesta IA con scan animation, agentes con orbiting nodes, presupuestos, clientes/proveedores, cashflow, calendario, informes IVA, generador, settings 18 secciones, mobile)
- 14 rutas, 0 errores TypeScript
- 7 commits en el repo

## Bloqueante

- **SQL schema no ejecutado contra Supabase Cloud** — archivos `supabase/migrations/001_schema.sql` (17 tablas) y `002_rls.sql` (RLS + funciones) escritos pero no aplicados
- No hay psql ni supabase CLI en la máquina local
- Ejecutar manualmente en Dashboard SQL Editor: `https://supabase.com/dashboard/project/lahqlyaxvobqjgdiftag/sql`

## Pendiente

- Fase 2: CRUD real conectando vistas a Supabase (tras ejecutar SQL)
- Fase 3: Generador funcional + PDF con @react-pdf/renderer + Cashflow real
- Fase 4: Ingesta multicanal (WhatsApp, Telegram, email, cámara) + Realtime + workflows n8n
- Fase 5: Agentes IA (cobros, copiloto, clasificador, IVA)
- Fase 6: Settings funcionales + búsqueda global + deploy Docker final
