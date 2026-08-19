---
title: aplicar migración por psql + registrar versión cuando el CLI de Supabase está bloqueado
date: 2026-07-19
source: claude-code-session
tags: [supabase, migraciones, red, psql]
---
Desde redes que bloquean los puertos Postgres (5432 / pooler 6543), `supabase
db push --linked` y `migration repair` CUELGAN — pero un `psql
"$SUPABASE_DB_URL" ...` directo SÍ conecta (usa otra ruta). Workaround para
aplicar una migración YA commiteada sin dejar huérfano:

1. `psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 -f supabase/migrations/NNN_x.sql`
2. Registrar la versión (equivalente a `migration repair --status applied`):
   `insert into supabase_migrations.schema_migrations (version,name)
    values ('NNN','x') on conflict (version) do nothing;`
   (columnas: version text, statements text[] nullable, name — con name basta.)

Mantén el formato **NNN** (no timestamp): el hook pre-push aborta si detecta
timestamps en el remote, y esta tabla ya viene en NNN. Verifica después:
`select proname from pg_proc where ...` + versión en `schema_migrations`.
Solo para migraciones additivas/`create or replace` (reversibles). No es
sustituto de `db push` cuando la red no está bloqueada.
Relacionado: la deuda "reconciliar migs timestamp" del hub venía de aplicar por
MCP (que grababa timestamp) — este método evita eso.

**El bloqueo es de PUERTO, no de host** (30-jul): con 5432/6543 en timeout,
`https://<ref>.supabase.co/rest/v1/…` con la service key seguía dando 200. Sirve
para **verificar sin acceso Postgres**: si una columna existe, o llamando a la
RPC con datos reales para comprobar el fix. Diagnóstico rápido antes de escalar:
`nc -z <pooler> 5432` KO + PostgREST 200 = es la red (VPN), no Supabase caído.
Y `db push` desde un worktree NO enlazado falla con `LegacyProjectNotLinkedError`
aunque copies `supabase/.temp` — hay que correrlo desde la raíz enlazada.

**Cuando psql TAMBIÉN cae (02-ago, red de un túnel de viento): SQL Editor del
panel**, pero con el `insert` en `schema_migrations` **dentro del mismo
`begin/commit` de la migración**. Si se registra aparte y algo falla arriba,
queda registrada sin estar aplicada, que es peor que no registrarla. Prepara un
fichero por migración (copia del original + el insert antes del `commit`) y una
consulta de verificación aparte: versiones registradas, que el objeto exista de
verdad en `pg_proc`/`pg_class`, y que no sea ejecutable por `anon`.
Gotcha que costó un diagnóstico falso ese día: **`psql -c "…"` con varias
sentencias es UNA transacción implícita** — si el último `select` falla por un
nombre de columna, se revierte también el `update` de arriba y parece un bug del
trigger. Una sentencia por `-c`, o `ON_ERROR_STOP` y fichero.

**Y pasó de verdad (6-ago): registrada sin aplicar.** El riesgo de arriba dejó de
ser teórico. Cómo se detecta y cómo se sale:
- No preguntes por la FILA, pregunta por el CONTENIDO:
  `pg_get_functiondef(p.oid) ILIKE '%<expresión nueva de esa migración>%'`, o la
  columna/constraint concreta. La versión en `schema_migrations` no prueba nada.
- Salida: `DELETE FROM supabase_migrations.schema_migrations WHERE version='NNN'`
  → aplicar el fichero → volver a registrar. **Aplicar primero, registrar
  después**, siempre.
- Y captura un hash de control antes/después de lo que NO debe moverse
  (`md5(string_agg(id||':'||precio, ',' ORDER BY id))`): una suma total puede
  compensar cambios entre sí, un hash no.

**Rematada (19-ago): guarda anti-carrera dentro del bloque, y verificación por PostgREST.**
Si otra sesión puede estar mergeando, el bloque manual lleva primero
`DO $$ IF EXISTS (select 1 from schema_migrations where version='NNN') RAISE EXCEPTION $$`
— con carrera, aborta entero en vez de registrar mentira. Y para un DROP, la verificación
independiente sin Postgres es PostgREST: `GET /rest/v1/<tabla>` → `PGRST205` = ya no existe.
Los PAT `sbp_` muertos también inutilizan la Management API (401): la vía manual es la única
cuando red+PAT fallan a la vez.
