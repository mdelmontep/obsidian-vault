---
title: git checkout <file> en el red-check deja el commit sin el fix (y build no compila tests)
date: 2026-07-05
source: claude-code-session
tags: [tdd, git, ci, testing, review]
---
TDD red-check: para ver el test fallar se revirtió el fix con `git checkout <file>`.
Eso restaura el fichero a HEAD (= sin fix, sin el `export` añadido). Si luego
commiteas sin RE-APLICAR, el PR queda solo con el test y el bug sigue vivo.

Doble trampa: `next build` NO typechecka/compila los ficheros de test → un test
que importa un símbolo inexistente **pasa el build**. Si tu único gate es build
(CI Actions caído, ver [[actions-sin-billing-hooks-locales-unico-gate]]), no lo caza.

Fix:
- Red-check con edición inversa reversible (sed/perl que revierte y RESTAURA), o
  `git stash`; NUNCA `git checkout <file>` sin re-aplicar el fix después.
- Antes de pushear: `git show --stat HEAD` debe incluir source + test.
- Corre el TEST (no solo build). El build es ciego a los ficheros de test.
- Un review independiente (maker≠checker) lo cazó aquí — vale su coste.
