---
title: supabase cloud — reglas para proyectos SaaS
date: 2026-04-20
source: claude-md-migration
tags: [supabase, saas, facturaia]
---

# Supabase Cloud (proyectos SaaS — FacturaIA etc.)

- **`psql` instalado**: `/usr/local/opt/libpq/bin/psql` (via `brew install libpq`, keg-only). Funciona para DDL/migrations contra Supabase Cloud
- **Conexión directa (`db.{ref}.supabase.co:5432`) solo IPv6** — si la máquina no tiene ruta IPv6, usar el connection pooler en su lugar
- **Connection pooler**: `postgresql://postgres.{ref}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres` — la region se descubre probando (FacturaIA: `eu-west-1`). Error "Tenant or user not found" = region incorrecta, no error de password
- **`sb_secret_*` / `sb_publishable_*` son keys de billing/plataforma** — no sirven para ejecutar SQL ni para la Management API. Access token para CLI debe ser formato `sbp_...` (Personal Access Token del dashboard)
- **Service role JWT solo funciona con PostgREST** — lectura/escritura de filas vía API REST, NO DDL (CREATE TABLE, ALTER, etc.)
