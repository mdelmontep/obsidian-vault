---
title: el script que renumera migraciones reescribe referencias a migraciones ajenas
date: 2026-08-14
source: claude-code-session
tags: [supabase, migraciones, tooling, docs, facturaia]
---

`mig:renumerar` sustituye tres patrones en los ficheros que **toca la rama**: `NNN_slug`,
`migNNNtoken` y `mig NNN`. Los dos primeros son inequívocos. El tercero no: `mig 677` puede
ser la migración que estás moviendo o **otra distinta que el fichero menciona de paso**, y
el script no los distingue.

En una tanda de 15 PRs pasó **cuatro veces** en un día: cada rama con migración `677_*` que
tocaba un manual o `CONTEXT.md` se llevó por delante referencias legítimas a la 677 de
marketing y a la 678 de api_keys, dejándolas apuntando a migraciones que no existen o que
son de otra cosa.

- El daño es **silencioso**: documentación que apunta a la migración equivocada, que es
  justo la pista que luego se sigue a ciegas en un incidente.
- Crece con el número de ramas simultáneas, porque todas tocan los mismos manuales.
- Tras renumerar, `grep 'mig 6[0-9][0-9]'` sobre los ficheros de la rama y verificar **una
  a una** contra `ls supabase/migrations`. El listado de "no supe traducir" que imprime el
  script NO las incluye: esas las traduce sin preguntar.
- Arreglo de raíz: sacar `mig NNN` del reemplazo automático y meterlo en ese listado.
