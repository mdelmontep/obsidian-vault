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

## Gotchas generales

- **Realtime requiere publicación explícita** — `ALTER PUBLICATION supabase_realtime ADD TABLE <tabla>` para cada tabla. Sin esto, los canales se suscriben pero nunca reciben eventos.
- **SQL functions con SELECT puro → `LANGUAGE sql`, no `plpgsql`** — si el body es un SELECT directo sin BEGIN/END. Con `plpgsql` da `syntax error at or near "SELECT"`.
- **`signUp` con email existente devuelve UUID falso** — protección anti-enumeración. Crear usuarios server-side con `admin.auth.admin.createUser()` usando service_role.

## Migrations CLI

- **`supabase db push` sin link falla** — ejecutar `supabase link --project-ref <ref>` primero
- **Migrations con nombres simples (001, 002) no sincronizan** — el CLI espera timestamps Unix. Si hay migrations remotas huérfanas: `supabase migration repair --status reverted <timestamp>`
- **`supabase db query --linked -f <file>`** — aplica SQL arbitrario contra el proyecto remoto. Forma fiable cuando `db push` falla por historial de migrations inconsistente
- **Joins implícitos requieren FK en mismo schema** — `audit_log.user_id → auth.users` (schema `auth`) no permite `.select('profiles(...)')`. Resolver con dos queries + merge manual en el cliente

## Storage — buckets y PDFs

- Bucket `facturas` (público, 5MB limit) en proyecto FacturaIA
- API route `generate-pdfs` usa service_role key via header `x-service-key` — permite ejecutar desde curl sin sesión de usuario
- Tabla `organizations` (inglés, no `organizaciones`) — el schema usa nombre en inglés
- FK `bandeja_ingesta.factura_id` → nullificar antes de delete facturas (`UPDATE bandeja_ingesta SET factura_id = NULL WHERE factura_id IN (...)`)
- PDFs generados con `pdf-lib` (no pdfkit) — ver [[pdf-lib-funciona-en-nextjs-turbopack-donde-pdfkit-falla]]
- `supabase/.temp/` — el CLI genera 8 archivos al linkear proyecto (gotrue-version, pooler-url, etc.). Añadir a `.gitignore` o contamina el contador de uncommitted
- **`ADD COLUMN ... DEFAULT false` no activa orgs existentes** — la columna se añade con el default pero las filas existentes quedan a `false`. Si el comportamiento esperado es opt-in-por-defecto, hacer UPDATE manual: `UPDATE tabla SET col = true WHERE col = false OR col IS NULL`
- **pgcrypto está en schema `extensions`, no `public`** — triggers con `SET search_path = public` no encuentran `digest()`. Fix: `SET search_path = public, extensions` y llamar `extensions.digest()` explícitamente
- **`jsonb_set(..., create_missing=true)` NO crea claves intermedias** — solo crea la última del path. Si `settings.whatsapp` no existe y haces `jsonb_set(settings, '{whatsapp,modos}', '[...]', true)`, falla silenciosamente (la clave intermedia `whatsapp` no se crea). Patrón seguro para deep merge: `settings || jsonb_build_object('whatsapp', COALESCE(settings->'whatsapp','{}'::jsonb) || jsonb_build_object('modos', '[...]'::jsonb))`. El `||` es shallow merge — para anidar hay que aplicarlo por nivel.
