---
title: mergear con --delete-branch CIERRA la PR apilada encima, no la re-apunta a main
date: 2026-08-12
source: claude-code-session agh-iberica
tags: [github, gh-cli, pr-apiladas, gotcha, proceso]
---
Con PRs apiladas (`B` tiene como base la rama de `A`, no `main`), la creencia extendida —y que yo
tenía escrita en tres sitios— es que al mergear `A` con `--delete-branch` GitHub re-apunta `B` a
`main`. **Medido: la CIERRA.** `B` queda `CLOSED` sin mergear y **no se puede reabrir**:

    gh pr reopen <B>  →  GraphQL: Could not open the pull request

porque su base ya no existe. Los **commits sobreviven** (la rama no se borra con la PR, y sobre el
`main` nuevo aporta exactamente los suyos), pero se pierden la PR, su cuerpo y su hilo de revisión:
hay que rehacerla desde la misma rama.

**El procedimiento que sí funciona**, en este orden:
1. mergear el padre **sin** `--delete-branch`;
2. `gh pr edit <hija> --base main` y comprobar `mergeable=MERGEABLE` **antes** de seguir;
3. mergear la hija; repetir;
4. borrar las ramas **al final**, cuando ya no son base de nada.

Y tras cada merge, `gh issue view <N> --json state`: si reescribiste el cuerpo de la PR, la línea de
cierre puede haberse ido con la cabecera — pasó en el mismo tramo y el issue quedó abierto.

De dónde salía la premisa falsa: de una línea que llevaba días en el snapshot del repo describiendo
una pila que **nadie había ejercitado**. La propagué a tres sitios sin medirla **porque ya estaba
escrita**: una premisa heredada se re-mide antes de propagarla, y más si vas a montar un
procedimiento encima.
