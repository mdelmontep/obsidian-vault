---
title: ponerle dientes al trinquete de contexto del vault
date: 2026-09-20
source: obsidian-vault
tags: [vault, harness, hooks, contexto]
---

`scripts/context-budget.mjs` hoy **no lo ejecuta nada**: el único `.git/hooks` del vault es un
`post-commit` que reindexa la BD de búsqueda y que nunca bloquea. Lo invoca una línea de prosa
dentro de `~/.claude/skills/obsidian-1/SKILL.md`, así que vive de que la skill se llame y de que
quien la corre no se salte el paso. Regla en prosa, no máquina.

Síntoma de que eso no basta, medido el 20-sep: `scripts/context-budget.json` llevaba días
**modificado sin commitear y hacia atrás** (el árbol con los valores del 5-sep, `HEAD` con los del
17-sep). Contra el baseline falso, `hub-facturaia` salía en verde con ▼ −0,5 KB; contra el real
había **crecido 3,0 KB**. Restaurado ese día; la copia del diff revertido quedó en el scratchpad de
la sesión.

**El hook obvio nace roto, y por eso esto no se hizo sobre la marcha:** el script mide **el árbol de
trabajo**, y el vault es un repo compartido por sesiones simultáneas → un `pre-commit` haría que el
crecimiento de `hot.md` de la sesión de FacturaIA **bloquee el commit de un learning de AGH**. Un
guard que se dispara por trabajo ajeno se desactiva en días. Mismo modo de fallo que
[[el-stop-hook-mide-el-arbol-y-un-barrido-de-mutacion-lo-pone-rojo]] y
[[un-hook-no-ve-variables-ni-la-version-de-main]].

**Lo que habría que construir:** que mida **lo que se está commiteando**, no el árbol — con el
truco de que `vault-commit` hashea el ÁRBOL y no el índice, así que la fuente correcta es el
contenido que va al commit, acotado a las rutas del commit. Y probarlo en el camino REAL (un commit
de otra sesión creciendo `hot.md` mientras tú commiteas en `knowledge/` **no** debe bloquear): los
casos que discriminan son ésos, no los de «no debe bloquear» triviales.
