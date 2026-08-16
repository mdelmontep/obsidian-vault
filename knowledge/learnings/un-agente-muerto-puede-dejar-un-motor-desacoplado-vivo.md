---
title: un agente muerto puede dejar un motor desacoplado vivo
date: 2026-08-16
source: claude-code-session
tags: [claude-code, subagentes, procesos, mutacion, higiene]
---

Un subagente murió por error de API. Había escrito un script driver en el scratchpad de la
sesión y lo había lanzado **desacoplado**: `ppid=1`, adoptado por `init`. Siguió corriendo
mutaciones sobre `src/` **1 h 56 min después de morir su agente**, con la máquina a load 40-60.

Las tres vías obvias fallan:
- **`pkill` sobre los hijos no sirve** — mueren y renacen, porque el motor los relanza. Al motor
  solo se llega **subiendo la cadena de `ppid`**, no mirando qué consume CPU.
- **`TaskStop` tampoco** — `No task found with ID`: un agente muerto no se para por su ID.
- **`mutate:restore` no repara** — el diario lo lleva `mutate:diff`, no el arnés invocado directo,
  así que el caso interrumpido (el único en que hace falta) no está cubierto.

Coste: un **fuente de producción quedó mutado en disco** y lo único que lo delataba era un
`git status` en un worktree que nadie miraba.

⚠️ Las dos lecturas fáciles son falsas: «sigue trabajando → el agente vive» y «el agente murió →
no corre nada». **Consulta el estado con `pgrep` + `ppid`**, no lo infieras del harness — y
después `git status` en TODOS sus worktrees antes de dar la limpieza por hecha. Al encargar un
barrido a un agente, prohíbele lanzar procesos desacoplados.
Hermano de [[agente-cortado-a-media-tarea-deja-trabajo-que-parece-terminado]].
