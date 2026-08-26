---
title: aplicar migraciones a prod antes del merge caduca la reserva de número
date: 2026-08-01
source: claude-code-session
tags: [supabase, migraciones, deploy, incidente, facturaia]
---

Un agente aplicó 6 migraciones a prod para poder tomar capturas. Antes de ramificar
verifiqué que ninguna rama viva usaba esos huecos: era cierto, y **caducó en dos horas**.
Otro PR mergeó su propia `607` y prod ya la tenía anotada con MI contenido → el siguiente
`db push` la habría dado por aplicada y **saltado en silencio** (8 orgs, 5 de clientes
reales, sin poder dar de alta 2ª empresa, con el deploy diciendo OK).

- El número se asigna **justo antes del merge** no por burocracia: porque "lo he
  comprobado" tiene fecha de caducidad mientras la rama vive.
- Lo paró el hook de `pre-push`, no una revisión humana. Cuarta vez que lo para él.
- **Reparar** (nunca editar `schema_migrations` a mano): `migration repair --status
  reverted <viejos>` y `--status applied <nuevos>`. El `reverted` corre desde cualquier
  checkout; el `applied` **exige los ficheros presentes**, así que hay que lanzarlo desde
  el worktree renumerado, copiándole `supabase/.temp/` entero (solo `project-ref` da
  `LegacyDbConfigIpv6Error`).
- Si el CLI pide `SUPABASE_DB_PASSWORD`: `op read` inline, no exportar.

Complementa [[migracion-numerar-contra-prod-schema-migrations]] (allí prod va por delante
por ramas ajenas; aquí la divergencia la causé yo).

**Quinta vez, y con motivo legítimo (06-ago, mig 651)**: apliqué como `650` para poder
`gen:types` y typecheckear contra el esquema nuevo. Mientras tanto se mergeó otra `650`
(obras), el `pre-push` obligó a renumerar a `651` y prod quedó con **una fila `650` cuyo
contenido era el de OTRA migración**. `migration list` no lo ve: compara versiones, no
contenidos. Lo que sí vale es comprobar **por catálogo** — `information_schema.columns` para
columnas y `pg_get_functiondef()` buscando una cadena única del cuerpo nuevo para funciones.
Prod tenía las dos, y la `651` se aplicó luego como no-op. Si necesitas los tipos antes del
merge: **`mig:renumerar` PRIMERO, `db push` después**. Y reaplicar solo es inocuo si la
migración es idempotente entera (`if not exists`, CHECK con guard, `is null` en cada paso del
backfill); si no lo es, no la apliques hasta después del merge.

**El otro lado de la misma regla (02-ago)**: aplicar antes cuida el NÚMERO, pero el
esquema hay que aplicarlo antes por otro motivo — **el código desplegado lo exige**.
Mergeé dos PRs y dejé el `db push` para el final; entre medias se cayó el pooler y prod
quedó llamando a una RPC inexistente → `/api/obras/materiales/familias` en 500. Hubo que
revertir los dos PRs. Orden bueno: `db push` → `migration list` para confirmar → merge.
Un `db push` que falla es razón para **parar el merge**, no un paso que se apunta para
luego. Y ojo con el orden inverso: el número se renumera justo antes de cada merge, así
que en una tanda de varios PRs con migración toca ir de uno en uno.

**Sexta vez, a TRES sesiones (15/17-ago, migs 693-703)**: dos sesiones renumerando en
círculo (693→696→697→698) mientras una tercera aplicaba por SQL editor con el pooler caído.
Tres piezas nuevas: (1) `mig:renumerar` es **fail-open** — sin leer prod avisa pero propone
número mirando solo el repo, y en un worktree NO lee prod ni con `SUPABASE_DB_PASSWORD` si
falta `supabase/.temp/` completo (el `pooler-url` es la conexión real): así nos propuso el
mismo número a dos sesiones. (2) La **propiedad** de una fila ya aplicada se desambigua por
CATÁLOGO, no por el registro: ¿existen en prod los objetos de TU migración? Si no, la fila es
de otro. (3) Lo que funcionó: el número se ocupa AL MERGEAR, coordinación explícita entre
sesiones (SendMessage), avisar SIEMPRE antes de aplicar a prod, y verificación cruzada por
nombre al cerrar. Prod por delante de main mientras un PR espera es ventana de colisión:
mergear rápido la cierra.

**Séptima vez, y el CLI propone MENTIR (26-ago, mig 761)**: otra rama sin PR abierto tenía
sus 756-760 ya aplicadas a prod. Dos bloqueos nuevos, ninguno en la lista de arriba:

1. `db push --linked` no se salta nada: **aborta** con `LegacyDbPushMissingLocalError`
   («remote migration versions not found in local migrations directory») y **sugiere
   `migration repair --status reverted 756 757 758 759 760`**. Eso sería declarar revertido
   lo que está aplicado: el registro pasaría a mentir y la siguiente rama las reaplicaría.
   Lo que sí vale: **copiar los ficheros de la otra rama a `supabase/migrations/` sin
   commitearlos**, `db push` (aplica solo el tuyo, los suyos ya constan) y borrarlos. Sin
   `--include-all`, que sí aplicaría de todo.
2. El `pre-push` corre `gen:types:check` contra el proyecto del checkout, así que main
   quedaba mintiendo sobre prod por columnas AJENAS y no había push posible sin regenerar.
   O cargas con la deriva del otro en un commit que diga de quién es, o bypasseas el hook.
   Se carga: el commit `chore(types)` con el porqué es barato; el bypass no.

Y otra vez la propiedad por catálogo antes de mover: en prod NO estaban mis objetos
(índice, trigger con DELETE, grants revocados) y SÍ `albaranes.creado_via` de su 759.
`mig:renumerar` se niega correctamente (issue #2095) cuando el número consta aplicado →
renumerar A MANO, actualizando también las cadenas `mig NNN:` de dentro del fichero.
