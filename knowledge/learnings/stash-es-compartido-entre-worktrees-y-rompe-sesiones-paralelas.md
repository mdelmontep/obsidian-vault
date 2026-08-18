---
title: el stash es compartido entre worktrees — una sesión paralela puede recuperar (y destruir) el trabajo de otra
date: 2026-07-27
source: claude-code-session
tags: [git, worktrees, agentes-paralelos, verificacion]
---
Los worktrees comparten el almacén `.git`, así que **el stash NO es local a la sesión**: un `git stash` creado en un worktree se puede hacer `pop` desde otro.

Caso real (agh-iberica, 2 subagentes en paralelo sobre el mismo `hitl-brain.ts`): el stash de la sesión A acabó en la B → **el fix de B desapareció** y su rama quedó con un commit que contenía el trabajo de A **bajo el mensaje de commit de B**. Detectado porque los tests seguían rojos con el fix «aplicado» y `grep` del símbolo nuevo no lo encontraba en ningún worktree. Nada llegó a `origin`, pero el gate del *otro* trabajo salía verde: se puede empujar código que no es el que dice ser.

**Tercera ocurrencia (facturaia, 31-jul) — con esta regla ya escrita, y la usé igual.** `git stash push -- <4 ficheros>` + `pop` para comparar un PDF antes/después: el `pop` **no devolvió lo mío, sacó un stash ajeno** y dejó 3 ficheros de otra sesión en conflicto `UU` dentro de mi worktree. La contaminación se limpió (`git restore --source=HEAD`, los 3 stashes intactos), pero lo grave fue silencioso: **el "antes" nunca llegó a aplicarse**, así que medí el fix contra sí mismo y concluí lo contrario de lo cierto ("el defecto es preexistente" cuando no lo era). Rehecho con un **worktree de control** —otra rama del mismo `origin/main`, sin el cambio— la conclusión se dio la vuelta. Si mides un antes/después, **verifica el estado del fichero antes de medir**, no confíes en que el stash se aplicó.

**Reglas:**
- **Cero `git stash`** en repos con worktrees paralelos. Para comparar contra la base: copiar a `/tmp`, `git checkout origin/main -- <fichero>`, medir, restaurar. Mejor aún si ya tienes otro worktree limpio: **mide ahí**, sin tocar nada.
- **El rojo-primero con `stash` sobre trabajo ya commiteado mide el fix contra sí mismo** (el stash no encuentra nada que guardar y no avisa) → salía «todo verde» con el fix puesto. Usar siempre `git checkout origin/main -- src/...`.
- Serializar los frentes que tocan el MISMO fichero de contratos, en vez de paralelizarlos.
- Tras cada subagente: `git show --stat HEAD` + `grep` del símbolo nuevo. Ver [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]].

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[un-baseline-que-mide-el-arbol-de-trabajo-hornea-el-wip-ajeno]] (el mismo árbol compartido, pero el que se lleva el trabajo ajeno es un trinquete que mide disco en vez de HEAD).
