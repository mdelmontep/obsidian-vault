---
title: regenerar tipos supabase con --linked, y desde la raíz enlazada — el redirect borra el fichero si falla
date: 2026-07-03
updated: 2026-09-05
source: claude-code-session
tags: [supabase, typescript, type-safety]
---
Al añadir una columna/tabla en un proyecto con tipos generados:

- Regenerar con `npm run gen:types` (usa `--linked`), NO con `--db-url`: la
  variante vieja borra el bloque `__InternalSupabase { PostgrestVersion }` de la
  cabecera y el fichero diverge del drift-check de CI. Con `--linked` el diff son
  SOLO las columnas nuevas.
- **Correrlo desde la raíz del repo enlazado, nunca desde un worktree**: el
  worktree no está linkado y el CLI muere con `LegacyProjectNotLinkedError`.
- **El script redirige con `>`, así que cuando el CLI falla escribe el JSON del
  error ENCIMA del fichero** y se lleva por delante las ~13.800 líneas de
  `database.types.ts` (31-jul). No lo delata el código de salida, que el redirect
  ya consumió: se detecta porque el `grep` de la tabla nueva da 0 en un fichero que
  debería tenerla. Verificar siempre el resultado, no el "ok".
- **CUÁNDO: después del `db push --linked`, no antes del merge.** El `--check` compara contra
  PROD, no contra el repo: un PR que aplica su migración tras mergear deja una ventana en la que
  `main` describe un esquema que prod no tiene, y el siguiente que empuje se come el rojo por un
  cambio ajeno (5-sep-2026, migs 844-846). Peor que el push roto: mientras los tipos van por
  detrás, el typecheck **no ve** lo que la migración rompió →
  [[una-fk-nueva-hacia-una-tabla-ya-referenciada-rompe-los-embeds-de-postgrest]].
- NO augmentar el `Database` global para una tabla o columna nueva: cambia la
  identidad estructural y dispara errores en CASCADA en ficheros ajenos. El patrón
  es vista tipada LOCAL al módulo que la escribe, y borrarla cuando `gen:types`
  traiga la tabla. Ver
  [[supabase-gen-types-numeric-override-bigint-string]].
- **Y el fichero puede mentir aunque el guard funcione**: un bloque pegado a mano pasa el
  typecheck y no se parece a una regeneración. El tell está en el diff →
  [[un-diff-de-fichero-generado-sin-danos-colaterales-no-salio-del-generador]].
