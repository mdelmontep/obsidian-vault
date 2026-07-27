---
title: un test nuevo no vale hasta que le rompes el código a propósito y falla
date: 2026-07-28
source: claude-code-session
tags: [testing, qa, metodo, verificacion]
---

Que un test pase no demuestra nada: puede estar saltándose, midiendo otra cosa o
afirmando algo que siempre es cierto. La comprobación barata es **romper a
propósito lo que dice vigilar** y confirmar que se pone rojo. Dos minutos.

Casos reales del mismo día en TuFacturaIA:
- Smoke de render de PDF: mutando `format: 'A4'` → `'A5'` en el renderer, **5 de
  7 tests** en rojo. Sin la mutación, solo sabía que 7 pasaban.
- Smoke del visor: reintroduciendo el bug exacto que lo motivaba (`flex: 1` sin
  altura en el iframe), falla con *"el visor mide 146px de alto"* — el 150 del bug
  original. Después, `git checkout` del fichero mutado.

Dos cosas que esto caza y el verde no:
- El test que **se salta** sin que nadie lo note (ver [[e2e-smoke-skip-honesto]]).
- El test que mide un artefacto vecino y no el que crees (el visor y el PDF son
  dos cosas distintas: uno puede estar perfecto y el otro roto dos meses).

Disciplina mínima: mutación **en el código de producción**, no en el test; una
sola mutación por vez; revertir antes de commitear (`git status` limpio salvo el
test). Y dejar escrito en el PR qué mutación se usó y qué falló — es la evidencia
de que el test sirve.
