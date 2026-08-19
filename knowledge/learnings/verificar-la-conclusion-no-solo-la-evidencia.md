---
title: verificar la conclusión, no solo la evidencia que la acompaña
date: 2026-08-19
source: facturaia
tags: [subagentes, verificacion, secretos]
---
Un agente concluyó que un `refresh_token` de Google en claro en un JSONB era «un permiso independiente
y **vivo**», de donde salía el plan «revocar antes de borrar». Su evidencia: lo descifró y comparó en
tiempo constante contra el token que guarda la plataforma, y **no coincidían**. Impecable. Y era la
comparación que no decidía.

Yo reproduje esa comparación, la vi correcta y **endosé la conclusión**. Falso: Google devuelve
`invalid_token` en `/revoke` (que no necesita credenciales de cliente, así que vale para cualquier token
de cualquier cliente) e `invalid_grant` en `/token` con las reales. Estaba **muerto**. No había nada que
revocar, y el «solo tú puedes hacer esto» que le pasé al usuario no existía.

**El salto era «no coincide con el respaldo» → «luego está vivo».** De ahí:

- **El estado de un secreto externo lo dice el proveedor, no la base de datos.** Se pregunta con una
  llamada, no se deduce de un `SELECT`.
- Al revisar a un agente, la pregunta no es «¿su evidencia es correcta?» sino **«¿su evidencia decide su
  conclusión?»**. Rigor sobre la pregunta equivocada se lee como rigor.
- Y usa dos señales que fallen por motivos distintos: aquí `/revoke` sin credenciales fue la que
  discriminó, porque `/token` a solas era ambiguo (otro cliente OAuth daría el mismo error).

Hermano de [[el-arnes-se-mide-a-si-mismo]] y de [[el-parte-de-un-job-caido-no-es-evidencia-de-lo-que-dejo]].
