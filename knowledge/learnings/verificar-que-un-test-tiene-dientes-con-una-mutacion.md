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

**La firma dominante: aserción negativa sin contraparte positiva** (1-ago, AGH — 15
casos verificados con mutación, **9 comparten esta forma**). «No ejecuta», «cero
acciones», «no contiene X» están verdes tanto si el código acierta **como si no hace
nada**. Ejemplos reales: un test cuyo comentario decía «el pending sigue vivo» solo
afirmaba «cero ejecutadas» — y eso lo cumple igual el turno retenido (correcto) que el
que DESCARTA el pending (el bug); otro se llamaba «re-propone» y lo cumplía un brain que
contestara «no te he entendido», dejando al usuario sin oír nunca la propuesta. El
arreglo es siempre el mismo: **añadir la mitad positiva** (que el outbound NOMBRE la
propuesta, que el pending SIGA ahí). Variantes hermanas: fixtures de tamaño 1, fakes
**ya ordenados** (ordenar por `createdAt` == por `occurredAt` si insertas en orden
cronológico) y tests **sin un solo `expect`** que cierran con un comentario.

**Y un guard es indetectable si su escenario no se puede construir**: un eval que usa la
MISMA instancia del proveedor para escribir y para leer nunca podrá detectar un desajuste
entre ambos — no es que falle, es que es estructuralmente ciego.

**Una mutación PARCIAL da falso verde, y se disfraza de «el test no vale»**
(31-jul, AGH): para probar que un caso de eval medía de verdad un argumento nuevo
del prompt, quité su mención de una línea… y el caso siguió 3/3. Parecía que
pasaba gratis. Había **cuatro** menciones; con las cuatro fuera, 0/3. Antes de
romper, **cuenta las ocurrencias** (`grep -c`) y comprueba que llegan a cero — si
no, no has medido el guard, has medido tu `sed`.
