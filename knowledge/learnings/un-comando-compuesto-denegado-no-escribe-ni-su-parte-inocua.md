---
title: un comando compuesto denegado no ejecuta ni la parte inocua que lo precede
date: 2026-09-10
source: facturaia
tags: [claude-code, harness, bash, permisos]
---
El clasificador (y cualquier hook de permisos) deniega **la llamada Bash entera**, no la
sentencia concreta que le molesta. Si en el mismo comando preparas el fichero y ejecutas la
acción vigilada, al denegarse **tampoco se escribe el fichero**, y no hay error que lo diga:
lo descubre el usuario cuando pega tu comando y le sale `No such file or directory`.

Medido el 10-sep-2026: un `cat > ajuste.sql <<'SQL' … SQL` seguido de `psql -f ajuste.sql`
contra prod. Denegado el `psql`, el `.sql` nunca existió; le pasé a Manuel un comando que
apuntaba a un fichero fantasma y perdimos un turno.

**Separa siempre la preparación de la acción vigilada en dos llamadas.** La preparación pasa
sola, y así el artefacto queda en disco listo para que lo ejecute quien pueda: tú tras un
permiso, o el usuario con `! <comando>` desde el prompt. Y cuando pases un comando al usuario,
comprueba antes que su fichero existe (`wc -l`), que es la mitad que el clasificador te dejó hacer.

Hermano de [[un-comando-denegado-suele-ser-un-hueco-en-la-allowlist]], pero al revés: allí la
denegación sobra y se amplía la allowlist; aquí es correcta y lo que falla es el empaquetado.
