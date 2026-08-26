---
title: supabase cloud — reglas para proyectos SaaS
date: 2026-04-20
source: claude-md-migration
tags: [supabase, saas, facturaia]
---

# Supabase Cloud (proyectos SaaS — TuFacturaIA etc.)

- **`psql` instalado**: `/usr/local/opt/libpq/bin/psql` (via `brew install libpq`, keg-only). Funciona para DDL/migrations contra Supabase Cloud
- **Conexión directa (`db.{ref}.supabase.co:5432`) solo IPv6** — si la máquina no tiene ruta IPv6, usar el connection pooler en su lugar
- **Connection pooler**: `postgresql://postgres.{ref}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres` — la region se descubre probando (TuFacturaIA: `eu-west-1`). Error "Tenant or user not found" = region incorrecta, no error de password
- **`sb_secret_*` / `sb_publishable_*` son keys de billing/plataforma** — no sirven para ejecutar SQL ni para la Management API. Access token para CLI debe ser formato `sbp_...` (Personal Access Token del dashboard)
- **Service role JWT solo funciona con PostgREST** — lectura/escritura de filas vía API REST, NO DDL (CREATE TABLE, ALTER, etc.)

## Gotchas generales

- **ENABLE RLS obligatorio en toda tabla nueva** — policies sin ENABLE = tabla pública. Verificar en Authentication > Policies. Tablas solo-service_role: ENABLE igualmente, sin policies. Ver [[supabase-enable-rls-olvidado-tabla-publica]]
- **La política tiene que nombrar la columna que decide visibilidad, y para columnas privadas hacen falta grants** — "el dueño ve su fila" no oculta un `internal=true` dentro de esa fila, y RLS no filtra columnas: `revoke select on t from authenticated` + `grant select (cols públicas)`. Caso real: mensajes internos de soporte legibles por el cliente en prod (mig 582). Ver [[rls-filtra-filas-no-columnas-y-la-politica-debe-nombrar-la-columna-privada]]
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

- **`postgres` NO puede el `grant` de `supabase_storage_admin`, pero SÍ puede crear las políticas de
  `storage.objects` y escribir en `storage.buckets`** (medido 17-ago-2026 en `tucrmia-prod`). El
  `grant` da `42501: role memberships are reserved` por Management API **y por el SQL Editor**, que
  corre con el mismo rol; de ahí **no se deduce** que `create policy` falle — son sentencias con
  requisitos distintos. Lo único del bloque que sí exige pertenencia es el `set local role <dueño>`
  que se suele copiar delante: quítalo. Esta deducción bloqueó una épica once días y generó un ticket
  a soporte innecesario. Sonda y detalle en
  [[postgres-de-supabase-no-puede-el-grant-de-storage-pero-si-crear-sus-politicas]]
- Bucket `facturas` (público, 5MB limit) en proyecto TuFacturaIA
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
- **`generateLink({type:'invite', email, options:{data, redirectTo}})` devuelve action_link sin disparar SMTP** — patrón para enviar email branded propio (Resend) en lugar del template Supabase. Acción atómica con createUser + INSERT membership previos. Aplica también a `type:'recovery'` (password reset) y `'magiclink'`. Además, el `hashed_token` devuelto se canjea en `POST /auth/v1/verify` (anon key, `type:'magiclink'`) → `access_token` real del usuario: patrón para smokes/tests autenticados sin conocer ni pisar su password (crítico si el usuario ya lo rotó). Ver [[supabase-bypassear-plantilla-auth-con-admin-generatelink]] + [[supabase-mint-access-token-sin-password-via-generate-link]].
- **`Site URL` es fallback silencioso** — si `redirectTo` enviado por el cliente NO está en la allowlist `Redirect URLs`, Supabase lo descarta y usa Site URL. Si Site URL apunta a `http://0.0.0.0:3000` (config dev olvidada), todos los emails de prod rompen sin error. Ver [[supabase-site-url-fallback-rompe-redirecturl-fuera-de-allowlist]].
- **Plantillas email Auth en Dashboard están en inglés** — Gmail marca banner rojo "External / Spam" porque dominio remitente + contenido genérico no cuadran. Bypass: `admin.generateLink` + envío propio Resend.
- **`auth.audit_log_entries` (audit trail nativo de GoTrue) puede estar completamente VACÍO en un proyecto con actividad real** — no asumir que Supabase Auth lo puebla por defecto; verificar con `select count(*) from auth.audit_log_entries` antes de diseñar cualquier feature encima (ej. mostrar logins en un feed de auditoría). Caso real 2026-07-04 (TuFacturaIA, 23 usuarios activos): 0 filas — obligó a descartar el plan de reusar esa tabla y dejar login/logout sin instrumentar hasta decidir una vía manual.

## Punteros recolocados desde hot.md (2026-07-27)

_Salieron del índice caliente al reservarlo a método/riesgo transversal; el learning está íntegro en `knowledge/learnings/`._

- **Borrado masivo por API (PostgREST/MCP) hace timeout con decenas de miles de filas** — ver [[supabase-borrado-masivo-api-timeout-lotes-ctid]]
- **`db push` sin output NO está colgado** — no matarlo asumiendo que espera password: comprobar con `supabase migration list`. Ver [[no-matar-un-db-push-lento-asumiendo-que-pide-password]]
- **Un guard de una migración ajena bloquea el `db push` entero** — ver [[db-push-lo-bloquea-el-guard-de-una-migracion-ajena]]
- **Dry-run de una migración contra prod, sin Docker**: concatenar los ficheros **quitando sus `BEGIN;`/`COMMIT;`**, envolver en `BEGIN; … SELECT de verificación; ROLLBACK;` y lanzarlo con `supabase db query --linked --file`. Valida sintaxis, DDL, backfills y guards **sobre los datos reales**, sin persistir nada — más útil que un replay local contra base vacía, donde los guards que cuentan filas reales no prueban nada. Ojo: el CLI devuelve **solo el último result set** (una consulta de verificación por ejecución) y hay que releer después, aparte, para confirmar que el ROLLBACK dejó todo igual.
- **`Remote migration versions not found in local migrations directory` casi nunca es deriva en prod: es tu rama vieja.** Antes de tocar nada, `git merge-base --is-ancestor <base-de-tu-rama> origin/main` y `git ls-tree -r --name-only origin/main supabase/migrations | tail`. Seguir la sugerencia del CLI (`migration repair --status reverted`) reescribe el historial de control de PROD para tapar que tu copia está desfasada — el arreglo exactamente equivocado. Caso real 27-jul: main había sido reescrita y el merge-base estaba 54 commits atrás; el fix era rama nueva desde `origin/main` + `cherry-pick` (rebase NO: intenta reproducir commits ajenos).
- **…pero a veces SÍ es deriva real en prod, y entonces bloquea a TODO el equipo.** 20-ago: prod tenía la mig `726` aplicada con su fichero **sin commitear**, suelto en el worktree de otra sesión → `db push` se plantaba para cualquiera, y `migration repair --status reverted 726` habría mentido (está aplicada de verdad). Se distingue con dos comandos: si `git ls-tree -r --name-only origin/main supabase/migrations | grep <NNN>` **y** `git log --all -S<NNN> -- supabase/migrations` salen vacíos, el fichero no existe en ningún commit → no es tu rama vieja, es un fichero que nadie ha subido. Salida sin tocar el historial de prod: aplicar la tuya con `db query --linked --file` (cuerpo + `INSERT` en `supabase_migrations.schema_migrations` + un `DO` que verifique y **aborte** en la misma transacción) y comprobar después por catálogo.
- **`db query --linked` sin IPv6**: si falla con `LegacyDbConfigIpv6Error`, `supabase link --project-ref <ref>` configura el pooler IPv4 y cachea la password (después ya no hace falta pasarla). Password inline desde 1Password, nunca impresa.

## Postgres — FKs y funciones (2026-07-29)

- **`ON DELETE SET NULL` en una FK COMPUESTA anula todas sus columnas**, incluida `org_id` (`NOT NULL`), así que borrar el padre falla con `23502` en vez de dejar el hijo sin padre. Postgres 15+: acotar con `ON DELETE SET NULL (columna)`. Ver [[fk-compuesta-on-delete-set-null-anula-todas-las-columnas]].
- **Para reescribir una función que ya corre en prod, extrae el cuerpo vivo** con `pg_get_functiondef`, no del fichero de migración que la creó: migraciones posteriores la han cambiado y publicar esa copia revierte lo posterior en silencio. Ver [[reemplazar-funcion-sql-extraerla-de-la-bd-no-del-fichero-de-migracion]].
- **Tabla hija nueva bajo una entidad fusionable → revisar la RPC de merge**, o el `DELETE` del duplicado se lleva sus filas por cascade. Ver [[merge-no-destructivo-reassign-por-store-y-delete-en-misma-tx]].
- **Un endpoint que muta varias tablas debe invalidar TODOS los dominios cacheados que tocó**, no solo el suyo. Ver [[use-cache-e4-endpoint-multi-tabla-invalida-solo-un-dominio]]
- **Una migración placeholder vacía no se nota hasta 123 migraciones después** — prod funciona y el agujero solo sale al levantar un entorno nuevo, con prisa. Detector: `grep -rl "Applied directly on remote" supabase/migrations/`. Ver [[migracion-placeholder-vacia-rompe-la-reconstruccion-y-no-se-ve-hasta-anos-despues]]
- **Migración con número ya aplicado en la BD = `db push` la SALTA en silencio** — el CLI decide por versión, no por contenido; el push sale verde y tu arreglo no se ha ejecutado. `migration list --linked`: fila con `local` vacío y `remote` con número = versión que nunca correrás. Ver [[colision-de-numero-de-migracion-hace-que-db-push-la-salte-en-silencio]]
- **`information_schema` no sirve para auditar permisos: solo enseña los tuyos** — 0 filas con un rol ajeno aunque los grants existan; mira `pg_attribute.attacl`/`pg_class.relacl`. Ver [[verificar-grants-por-columna-con-pg-attribute-attacl-no-con-information-schema]]
- **Filtrar en el endpoint no es filtrar: la política tiene que nombrar la columna privada** — y ningún RLS oculta columnas, eso son grants. Ver [[rls-filtra-filas-no-columnas-y-la-politica-debe-nombrar-la-columna-privada]]
- **Columna jsonb con varios escritores: cualquier PATCH parcial es un borrado** — si N sitios escriben la misma columna y uno hace upsert de "lo que yo conozco", borra las claves ajenas. Inventariar escritores por nombre de columna; merge por clave + allowlist + borrado solo explícito. Ver [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]] · [[ADR-039-org-module-config-patch-merge-con-allowlist]].
- **Un worktree por PR = el CLI de Supabase ve divergencia y aborta el push** — ninguno tiene la foto completa de migraciones, y el link vive en `supabase/.temp` (gitignored). Ver [[migraciones-repartidas-entre-worktrees-dan-falsa-divergencia]]

- **Un `update` que afecta a cero filas NO devuelve error.** RLS que filtra la fila, `id` inexistente o estado ya cambiado → 204 con `error === null`, y el endpoint responde `{ok:true}` sobre una escritura que no ocurrió. El update tiene que pedir la fila de vuelta (`.select('id').maybeSingle()`) y tratar `data === null` como conflicto. Ver [[update-que-afecta-cero-filas-no-devuelve-error-en-postgrest]]

## Privilegios y RLS (03-ago-2026)

- **`TRUNCATE` no pasa por RLS** y sobrevive a un `revoke update, delete`: vacía la tabla de todas las
  organizaciones. Revocar los cuatro DML **enumerados** sobre el `grant all` de Supabase deja vivos
  `TRUNCATE`, `REFERENCES`, `TRIGGER` y `MAINTAIN`. Los privilegios se conceden por enumeración, **no se
  quitan** por enumeración: `revoke all` y conceder lo justo, cerrando también los `alter default
  privileges`. Comprobar el ACL efectivo (`relacl`), nunca el texto de la migración. Ver
  [[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]
- **Una membresía `'invited'` con políticas que exigen `'active'`**: el usuario entra con sesión válida y
  ve **cero filas**, sin error. Mirar qué exige la política antes de elegir el estado inicial. Ver
  [[membresia-invitada-con-politicas-que-exigen-activa-entra-y-no-ve-nada]]
- **`generate_link` devuelve `action_link` y `hashed_token`, y no dan lo mismo**: el primero resuelve la
  sesión en el navegador (fragmento `#access_token`), el segundo permite canjearla en el servidor con
  `verifyOtp` y dejarla en cookies `HttpOnly`. Ver
  [[enlace-de-acceso-canjeado-en-el-servidor-con-hashed-token]]
- **Leer prod sin poder escribir: `BEGIN READ ONLY`, no `SET SESSION`** — con el pooler ni `SET SESSION
  characteristics` ni `options=-c` persisten, así que el candado que crees puesto no está. Prueba el
  candado con una escritura REAL sobre una tabla de negocio, no con un `CREATE TEMP TABLE` (que un
  read-only sí permite y te da un falso verde). Y el rol de lectura `claude_runner_ro` NO sirve para
  medir: sin `BYPASSRLS`, las tablas con RLS devuelven **0 filas en silencio**. Ver
  [[set-session-read-only-no-persiste-en-el-pooler-usa-begin-read-only]]
- **Un ajuste de Auth se acepta con 200 y NO se aplica.** `security_update_password_require_current_password`
  volvió `false` al releer, sin error. La regla que ya teníamos para Dokploy —«200 y releer no significa
  aplicado»— vale igual aquí: **relee siempre tras escribir en `PATCH /v1/projects/<ref>/config/auth`**.
  El hueco lo cubre `security_update_password_require_reauthentication`, que sí se aplica.
- **`smtp_port` se tipa como TEXTO** («expected string, received number») y es el único numérico que lo hace
  —`password_min_length`, `mailer_otp_exp` y `rate_limit_email_sent` sí son números—. Declararlo como número
  falla al escribir Y deja cualquier comparador en rojo permanente si el `GET` devuelve `"587"`.
- **Dos protecciones son de pago**: `password_hibp_enabled` (contraseñas ya filtradas) exige **Pro** (402), y
  `hook_password_verification_attempt` exige **Teams**. En plan free, contra la fuerza bruta sólo queda su
  límite por IP o un captcha. Ver [[un-limite-delante-de-tu-accion-no-protege-si-la-operacion-es-publica]]
- **Sin SMTP propio el correo NO llega a un cliente**: el remitente integrado sólo entrega a miembros del
  equipo del proyecto, y con `rate_limit_email_sent: 2` **dos peticiones agotan la cuota de todo el proyecto
  durante una hora** — denegación de servicio trivial y sin autenticar. Comprobar credenciales SMTP sin
  enviar nada: handshake `EHLO`/`STARTTLS`/`AUTH LOGIN` y esperar `235`.
- **`disable_signup: false` es el defecto y deja `POST /auth/v1/signup` ABIERTO** con la clave anónima.
  Discriminar sin crear usuario: mandar una contraseña de un carácter — si contesta `weak_password`, el
  registro está abierto; si contesta `signup_disabled`, cerrado.

## Movido desde `hot.md` (poda del 14-ago)

Estaban en el índice de arranque, que se paga en TODA sesión sin disparador claro, y la regla del propio `hot.md` dice que un gotcha de un stack concreto no entra ahí: su casa es este fichero, que ya se carga cuando tocas lo suyo.

- **Filtrar por línea un volcado SQL BORRA datos** — un `grep -v '^--'` sobre un `pg_dump` se come las líneas de HTML/SQL de ejemplo que van dentro de un INSERT multilínea. Aquí saltó como error de sintaxis; sobre otro texto habría entrado limpio y mutilado. Anclar el patrón y filtrar la cabecera solo hasta el primer INSERT. Ver [[filtrar-por-linea-un-volcado-con-valores-multilinea-borra-datos]]
- **`psql -f fichero.sql` devuelve 0 aunque un `RAISE EXCEPTION` aborte el script entero.** Un validador
  SQL que imprime «ERROR: el caso (a) lo dejó en 0» sale con `$?` = 0, así que un arnés que solo mira el
  código de salida da verde sobre un fallo que está en pantalla. Se arregla con `-v ON_ERROR_STOP=1` (no
  con `\set ON_ERROR_STOP on` dentro del fichero, que además hace fallar `supabase db query` con 42601).
  Misma familia que el `push | tail` que devuelve el exit del pipe: el veredicto se lee de donde no está.
- **`gen:types:check` puede abortar el push de CUALQUIER rama sin que nadie haya tocado el esquema**: el
  fichero de tipos lleva `__InternalSupabase.PostgrestVersion`, y cuando Supabase actualiza PostgREST en el
  proyecto (26-ago-2026: `14.5` → `14.17`) el guard salta para todo el mundo. Antes de buscar qué migración
  lo rompió, `git diff origin/main..HEAD -- <ruta de tipos>`: si sale vacío, la deriva es de plataforma y el
  arreglo es regenerar y commitear esa línea. No se bypasea el hook.
