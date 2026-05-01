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

- **ENABLE RLS obligatorio en toda tabla nueva** — policies sin ENABLE = tabla pública. Verificar en Authentication > Policies. Tablas solo-service_role: ENABLE igualmente, sin policies. Ver [[supabase-enable-rls-olvidado-tabla-publica]]
- **Realtime requiere publicación explícita** — `ALTER PUBLICATION supabase_realtime ADD TABLE <tabla>` para cada tabla. Sin esto, los canales se suscriben pero nunca reciben eventos.
- **SQL functions con SELECT puro → `LANGUAGE sql`, no `plpgsql`** — si el body es un SELECT directo sin BEGIN/END. Con `plpgsql` da `syntax error at or near "SELECT"`.
- **`signUp` con email existente devuelve UUID falso** — protección anti-enumeración. Crear usuarios server-side con `admin.auth.admin.createUser()` usando service_role.
- **Invitaciones — no depender del trigger `handle_new_user`** — `inviteUserByEmail({data})` no siempre propaga `data` a `raw_user_meta_data`. Crear `org_member` directamente con upsert tras invitar (`estado: 'invitado'`), aceptar `'invitado'` en sesión y promover a `'activo'` en el primer login. Ver [[supabase-inviteuserbyemail-no-propaga-data-a-raw-user-meta-data]]
- **Templates con tokens en PL/pgSQL** — `replace()` deja literal lo desconocido. Validar con CHECK + función `is_valid_*` en BD, en API (allowlist TS) y UI. Ver [[postgres-template-tokens-replace-simple-no-rechaza-desconocidos]]
- **Sanitizar caracteres en `.or()` y `.ilike()`** — `%_,():.\\*"` son sintaxis PostgREST. Antes de pasar `q` del usuario: `q.replace(/[%_]/g, c => '\\' + c).replace(/[,():.\\*"]/g, ' ')`. Sin esto, comillas o paréntesis en search rompen la query o permiten inyección lógica.
- **`NOTIFY pgrst, 'reload schema';` al final de migrations con columna nueva** — sin él PostgREST responde 404 `PGRST204` en INSERTs aunque SELECT lea bien. Ver [[postgrest-schema-cache-notify-tras-migration]]

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
- **`as any` en `.from()` oculta typos de columna** — cuando `database.types` no incluye una tabla nueva (porque `gen types` no se ha corrido tras la migración) y usas `(supabase.from('tabla') as any).select('campo_inventado')`, el typecheck pasa y solo descubres el error al primer runtime ("column does not exist"). Tras añadir tabla nueva: regenerar tipos (`supabase gen types typescript --linked > src/types/database.types.ts`); si no se puede (cuenta sin permisos en proyecto compartido), auditar manualmente nombre por nombre contra el archivo de migración antes de mergear. Bug real: `clients.contact_email` vs `primary_contact_email` en agency-portal PR-P5
