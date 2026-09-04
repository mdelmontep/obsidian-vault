---
title: supabase migration número colisión entre ramas — renumerar
date: 2026-06-30
source: claude-code-session
tags: [supabase, migrations, git]
---

**Síntoma**: `supabase db push --linked` dice "Remote database is up to date" pero la columna no existe. La migración NNN local colisiona con una NNN remota de otra rama ya mergeada.

**Por qué**: `schema_migrations` registra versiones por número. Si la rama A mergea `418_foo` antes que la rama B, el `418_bar` de B queda "marcado como aplicado" sin ejecutarse nunca.

**Fix**:
1. `git mv NNN_nuevo.sql NNN+1_nuevo.sql` + actualizar cabecera `-- NNN_` en el archivo
2. Crear placeholder `NNN_nombre-real.sql` (solo comentario) para la migración remota huérfana
3. `supabase migration repair --status applied NNN --linked`
4. `supabase db push --linked` → aplica `NNN+1`
5. Commit: `git add` ambos archivos + push

**Prevenir**: asignar el número justo antes del **MERGE** — no al crear la rama ni al abrir el PR: mientras el PR espera, otro se lleva el hueco. Y con script, no a ojo (en TuFacturaIA, `npm run mig:renumerar`).

**El destino es máximo+1, NO el primer hueco** (2026-08-01): los huecos de la secuencia suelen estar **reservados por PRs abiertos sin mergear**, así que ir al primero te manda justo a la colisión que querías evitar. Ese día faltaban el 603 y el 605 en `main` y los tenía un PR pendiente.

**El hueco caduca en minutos, no en días** (1-ago, misma sesión): asigné el 620, y mientras corría el gate otra sesión mergeó su propio 620. Renumerar a 621/622 obligó a traer `main` y rehacer el gate. O sea que «justo antes del merge» es literal: entre asignar el número y mergear no cabe una tanda de tests. Y lo que lo pilló no fue el hook, fue comprobar a mano `origin/main` y `supabase migration list --linked` inmediatamente antes de mergear. Si el PR espera, se vuelve a comprobar.

**Al limpiar ramas: que tu número no esté en main NO significa que tu migración no esté** (3-ago). La rama `probar-migraciones` traía `578_defaults_uuid_ossp_a_gen_random_uuid.sql` y `579_extensiones_esquema_explicito.sql`, y en `main` el 578 y el 579 son otras dos migraciones distintas → el chequeo por fichero decía «no está en main» y sus propios commits decían «SIN VERIFICAR, no mergear». Parecía trabajo sin subir. Habían entrado **renumeradas a 580 y 581**, y el único diff era el marcador que reescribe el script. Compara por CONTENIDO ignorando el número, no por nombre de fichero.

**Y cuidado con que el script se cuente a sí mismo**: el de TuFacturaIA metía `git ls-files` —que incluye la migración nueva de la rama— en el conjunto de ocupados, así que con main en 606 y una local 607 proponía el 608, y cada pase volvía a empujar (608 → 609…). De ahí venía la regla «córrelo UNA sola vez»: un parche de memoria humana sobre un off-by-one. Arreglado excluyendo las migraciones de la propia rama → idempotente. **Si una herramienta trae una regla de uso del tipo «no lo corras dos veces», sospecha de la herramienta antes que de tu memoria.**

**El script no ve las ramas remotas ajenas** (4-sep, facturaia, mig 833 → 836). `mig:renumerar --dry` dijo «833 ya está en su hueco» mientras el #2503, ya empujado, llevaba el 833 y el 834. El script cuenta prod + `origin/main`; una rama empujada sin mergear es invisible para los dos. Y como `db push` decide por VERSIÓN y no por contenido, su silencio tampoco es prueba: se la salta sin error. El barrido que sí lo ve, antes de aceptar el número:

```
for b in $(git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||'); do
  git ls-tree -r --name-only origin/$b supabase/migrations 2>/dev/null
done | grep -oE '^supabase/migrations/[0-9]{3}' | sort -u | tail -5
```

**Y un número que otra sesión te anuncia no es una medición.** Ese mismo día una sesión paralela avisó de que tomaba el 835 y el 836 cuando el 836 ya estaba aplicado a prod y mergeado. Se paró con tres medidas, no con el aviso: `max(version)` de prod, el fichero en `origin/main`, y el barrido de arriba. Al renumerar a mano, quitar el número de los IDENTIFICADORES de dentro (bloques `$dollar$`, códigos de prueba, nombres de scratch) y dejarlo solo en las CITAS — si no, el fichero renumerado sigue diciendo el número viejo por dentro.
