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
2. `gh pr edit <hija> --base main`;
3. **`git rebase --onto origin/main <rama-padre>`** en la hija + `push --force-with-lease`, y comprobar
   `MERGEABLE` **después** del rebase;
4. mergear la hija; repetir;
5. borrar las ramas **al final**, cuando ya no son base de nada.

⚠️ **Corrección del 14-ago: el paso 2 no basta y su comprobación da un verde FALSO.** Re-apuntar la base
arregla **la base de la PR, no su historia**: el padre entró por **squash**, así que sus commits no son
ancestros de `main` y la hija diverge aunque el árbol coincida. Medido con un padre y dos hijas: una
salió `CONFLICTING`… y **la otra `MERGEABLE`**, porque su contenido ya coincidía y git sabía fusionarlo
— **mergearla habría metido el diff del padre OTRA VEZ** dentro de su commit de squash. 👉 **`MERGEABLE`
no significa «lista», significa «git sabe combinarlo»**: rebasar igual y comprobar que
`gh pr diff <hija> --name-only` trae **solo lo suyo**. El `rebase --onto` ya estaba escrito desde el
13-jul en [[pr-apilado-squash-cierra-al-borrar-base]]; aquí faltaba.

Dos cosas más que la pila obliga a medir aparte: la **combinación de dos hermanas nunca se ha compilado**
(gate sobre las dos juntas), y si una toca la vista mientras la otra le cambia debajo un artefacto que su
sonda consume (una baseline, un formato de clave), **la evidencia de navegador de la primera caduca** al
rebasar — hay que re-correrla, no re-correr el gate.

Y tras cada merge, `gh issue view <N> --json state`: si reescribiste el cuerpo de la PR, la línea de
cierre puede haberse ido con la cabecera — pasó en el mismo tramo y el issue quedó abierto.

De dónde salía la premisa falsa: de una línea que llevaba días en el snapshot del repo describiendo
una pila que **nadie había ejercitado**. La propagué a tres sitios sin medirla **porque ya estaba
escrita**: una premisa heredada se re-mide antes de propagarla, y más si vas a montar un
procedimiento encima.
