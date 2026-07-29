---
title: el nombre de la variable no es su procedencia, y una premisa sin verificar produce un fix para un caso imposible
date: 2026-07-30
source: claude-code-session
tags: [metodo, runner, facturaia]
---

Leí `const branch = \`fix/ticket-${id8}\`` y concluí que la rama era determinista **por ticket**. De ahí
salió un arreglo entero: buscar el PR existente y manejar el "already exists" de `gh pr create` en un
relanzamiento. Lo escribí en el cuerpo del PR y lo defendí dos veces con seguridad.

Era falso. `const id8 = job.id.slice(0, 8)` — el id del **JOB**, no del ticket (`job.id` ≠
`job.ticket_id`), y cada relanzamiento crea un job nuevo. La rama siempre fue única por EJECUCIÓN, así
que el caso que arreglé no era alcanzable y hubo que borrar ese código en el commit siguiente. Un
revisor externo construyó encima otro hallazgo sobre la misma premisa, así que el error se propagó.

El literal `fix/ticket-` me hizo asumir la procedencia del valor. Dos líneas arriba estaba la verdad.
Regla: antes de construir sobre "X es único/determinista por Y", **sigue el valor hasta su origen**,
no leas su nombre. Y si la premisa sostiene un fix entero, verificarla es parte del fix, no un extra.
Señal de alarma: estás escribiendo el porqué en el cuerpo del PR con más seguridad que evidencia.

Ver [[mide-el-reparto-de-fallos-antes-de-arreglar-el-que-te-cuentan]]
