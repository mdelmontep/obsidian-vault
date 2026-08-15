---
title: un candado nuevo en main caza las PRs abiertas escritas antes que él, y ningún gate individual lo ve
date: 2026-08-15
source: claude-code-session agh-iberica
tags: [testing, merge, gate, metodo, ci]
---
Al mergear once PRs en un día, el gate de la **combinación** dejó `main` en rojo: el candado de
exports fantasma cazó una constante exportada sin consumidor de producción, en una PR que **no
estaba mal**.

**Ninguna de las dos PRs podía verlo.** El candado llegó a `src/` en una PR mergeada *después* de
que la otra se escribiera — su gate (medido cuatro días antes) no podía conocerlo, y el gate de la
que traía el candado tampoco, porque su diff no tocaba ese fichero. **El defecto solo existe al
juntarlas.**

👉 La regla nueva: **cuando un candado nuevo entra a `main`, todas las PRs abiertas escritas antes
son candidatas a caer en él — no por estar mal, sino por ser anteriores.** Antes de un tren de
merges, mira qué candados han entrado desde que se escribió cada rama; no basta con que su gate
estuviera verde.

Corolarios que ya son doctrina y aquí se cobraron en vivo:
- **El gate de una rama no dice nada de la combinación.** Compila las ramas juntas ANTES de mergear
  (worktree aparte, `merge` de todas, `tsc`), y corre el gate **sobre `main` ya mergeado**.
- Una línea de gate **caduca**: las ajenas eran de 3-5 días antes y ninguna valía.
- El acoplamiento **no lo enseña la lista de ficheros**: aquí eran disjuntas fichero a fichero
  (`comm` vacío) y aun así se rompían. Igual que la dependencia por `import`.

Ver [[el-gate-verde-no-es-la-revision-mutar-lo-que-el-diff-cambia]] ·
[[delete-branch-al-mergear-cierra-la-pr-apilada-no-la-reapunta]].
