---
title: regenerar tipos supabase con --linked, nunca augmentar el Database global a mano
date: 2026-07-03
source: claude-code-session
tags: [supabase, typescript, type-safety]
---
Al añadir una columna en TuFacturaIA (o cualquier proyecto con tipos generados):

- Regenerar con `npm run gen:types` (que usa `--linked`), NO con
  `supabase gen types --db-url`: la variante `--db-url` (CLI vieja) borra el
  bloque `__InternalSupabase { PostgrestVersion }` de la cabecera → el fichero
  diverge de lo que produce el drift-check de CI (`gen:types` + `git diff
  --exit-code`). Con `--linked` el diff son SOLO las columnas nuevas.
- NO augmentar el tipo `Database` global en `database-overrides.ts` con
  `Omit<GenTables, 'tabla'> & { tabla: ... }` para una columna nueva: cambia la
  identidad estructural del tipo y dispara errores de asignabilidad en CASCADA
  en ficheros ajenos (p. ej. `fiscal_declaracion_snapshot.base_x100`
  string|number vs number en cashflow/ocr). Regenerar los tipos reales es la
  vía; overrides solo para los fixes numéricos ya existentes.
