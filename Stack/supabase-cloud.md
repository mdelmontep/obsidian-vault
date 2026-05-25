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
- **`.maybeSingle()` devuelve null sin throw visible si hay >1 filas** — solo seguro con constraint UNIQUE. Si la query puede tener múltiples matches, usar `.limit(1).order(...)` explícito. Ver [[supabase-maybesingle-devuelve-null-si-multiples-filas]]
- **`.or()`/`.eq()` con `+` en el valor desde REST manual requiere `%2B`** — cliente JS lo encoda solo; curl/fetch directos no. Síntoma: query devuelve 0 filas aunque la fila exista. Ver [[postgrest-or-con-plus-url-encoding]]
- **Leer credenciales cifradas en BD prod desde local sin pegarlas en chat** — helper Node carga `.env.local`, fetch a `platform_credentials` con `SUPABASE_SERVICE_ROLE_KEY`, descifra con `CREDENTIAL_ENCRYPTION_KEY` (AES-256-GCM, formato `v1:iv:tag:ct` base64url) y emite plaintext a stdout. Wrapper bash: `SECRET="$(node scripts/_get-secret.mjs)" bash smoke.sh`. Valor nunca pasa por chat ni stdout visible.

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
- **Embed via FK simple (`cliente:clientes(id, nombre)`) tipa array, runtime objeto** — supabase-js no infiere cardinalidad sin metadata, así que tipa como `[]` aunque el runtime devuelve objeto único. Cast defensivo: `Array.isArray(x) ? (x[0] ?? null) : x`. Aplica a todo embed por FK simple. Ver [[supabase-js-fk-embed-tipa-array-pero-runtime-objeto]]
- **`CREATE OR REPLACE VIEW` falla tras `ALTER TABLE` que añade columnas si la view usa `f.*`** — error `42P16: cannot change name of view column "X" to "Y"`. Las posiciones de columnas en `*` cambian al añadir columnas a la tabla base, y CREATE OR REPLACE exige mismo nombre+orden. Solución: `DROP VIEW IF EXISTS` + `CREATE VIEW` (no replace). Tras `CREATE`, reaplicar `ALTER VIEW ... SET (security_invoker = true)` para Postgres 15+ — sin esto la vista bypassea RLS del caller.
- **Embedded selects de Supabase JS (`select '*, otra_tabla(*)'`) NO funcionan sobre views** — requieren FKs declaradas, y las vistas no propagan FKs aunque las tablas base las tengan. Para combinar datos de una vista con joins: 2 queries en paralelo + merge en cliente: `const map = new Map(rows2.map(r => [r.id, r])); rows1.map(r => ({...r, ...map.get(r.id)}))`.
- **Migration con NOT NULL en columnas nuevas: secuencia obligatoria en la misma migration** — `ALTER TABLE ... ADD COLUMN x text` (nullable) → `UPDATE ... SET x = ...` (backfill desde otras columnas con CASE) → `ALTER TABLE ... ALTER COLUMN x SET NOT NULL`. Si dejas el SET NOT NULL para "después", las escrituras nuevas se cuelan con NULL y rompes la disciplina. Hacerlo todo en una sola migration es atómico y seguro.
- **Lookup de `profiles` por phone/email para audit cross-canal DEBE scoping vía `org_members!inner`** — sin esto, un mismo teléfono o email registrado en otra org se atribuiría al user equivocado (cross-tenant impersonation latente). Patrón: `.from('profiles').select('user_id, ..., org_members!inner(org_id, estado)').eq('phone', x).eq('org_members.org_id', orgId).eq('org_members.estado', 'activo')`. Aplicable a webhook receivers, agentes voz/email, cualquier resolución de identidad por dato externo.

## Auth Admin (Supabase Auth)

- **`admin.auth.admin.signOut(userId)` default scope='global' pero solo revoca refresh tokens** — el access JWT actual sigue válido hasta su expiración natural (~1h). Si revocas membresía y rediriges a `/login` basado en `!orgId`, el middleware ve `user` truthy y vuelves a `/dashboard` → loop. Fix: página fallback `/sin-acceso` para autenticados sin org operable. Ver [[signOut-solo-invalida-refresh-no-access-token]] + [[ADR-007-sin-acceso-fallback-vs-loop-redirect]].
- **`createUser({email, email_confirm:false})` dispara trigger `handle_new_user` síncrono** — el trigger inserta `profiles` con default vacío. Para invitaciones atómicas (createUser + INSERT membership + email link): orden estricto + rollback con `admin.auth.admin.deleteUser` si el email falla. Sin rollback de auth.users, queda zombie y la próxima invitación al mismo email devuelve `user_exists`. Recovery: detectar mensaje y devolver 409 `user_exists_retry` al cliente. Ver [[supabase-createuser-race-trigger-handle-new-user]].
- **`generateLink({type:'invite', email, options:{data, redirectTo}})` devuelve action_link sin disparar SMTP** — patrón para enviar email branded propio (Resend) en lugar del template Supabase. Acción atómica con createUser + INSERT membership previos. Aplica también a `type:'recovery'` (password reset) y `'magiclink'`. Ver [[supabase-bypassear-plantilla-auth-con-admin-generatelink]].
- **`Site URL` es fallback silencioso** — si `redirectTo` enviado por el cliente NO está en la allowlist `Redirect URLs`, Supabase lo descarta y usa Site URL. Si Site URL apunta a `http://0.0.0.0:3000` (config dev olvidada), todos los emails de prod rompen sin error. Ver [[supabase-site-url-fallback-rompe-redirecturl-fuera-de-allowlist]].
- **Plantillas email Auth en Dashboard están en inglés** — Gmail marca banner rojo "External / Spam" porque dominio remitente + contenido genérico no cuadran. Bypass: `admin.generateLink` + envío propio Resend.
