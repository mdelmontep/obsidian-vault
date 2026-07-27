---
title: el stash es compartido entre worktrees — una sesión paralela puede recuperar (y destruir) el trabajo de otra
date: 2026-07-27
source: claude-code-session
tags: [git, worktrees, agentes-paralelos, verificacion]
---
Los worktrees comparten el almacén `.git`, así que **el stash NO es local a la sesión**: un `git stash` creado en un worktree se puede hacer `pop` desde otro.

Caso real (agh-iberica, 2 subagentes en paralelo sobre el mismo `hitl-brain.ts`): el stash de la sesión A acabó en la B → **el fix de B desapareció** y su rama quedó con un commit que contenía el trabajo de A **bajo el mensaje de commit de B**. Detectado porque los tests seguían rojos con el fix «aplicado» y `grep` del símbolo nuevo no lo encontraba en ningún worktree. Nada llegó a `origin`, pero el gate del *otro* trabajo salía verde: se puede empujar código que no es el que dice ser.

**Reglas:**
- **Cero `git stash`** en repos con worktrees paralelos. Para comparar contra la base: copiar a `/tmp`, `git checkout origin/main -- <fichero>`, medir, restaurar.
- **El rojo-primero con `stash` sobre trabajo ya commiteado mide el fix contra sí mismo** (el stash no encuentra nada que guardar y no avisa) → salía «todo verde» con el fix puesto. Usar siempre `git checkout origin/main -- src/...`.
- Serializar los frentes que tocan el MISMO fichero de contratos, en vez de paralelizarlos.
- Tras cada subagente: `git show --stat HEAD` + `grep` del símbolo nuevo. Ver [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]].

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]].
