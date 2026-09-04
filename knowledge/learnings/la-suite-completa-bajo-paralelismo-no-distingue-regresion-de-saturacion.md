---
title: la suite completa bajo paralelismo no distingue una regresión de una saturación
date: 2026-08-16
source: claude-code-session
tags: [tests, ci, cpu, gate, falso-positivo]
---

Tres corridas de la MISMA suite sobre el mismo árbol dieron **tres conjuntos distintos de rojos**
(1, 18 y 7 ficheros) **sin un solo fichero en común**. Los 41 implicados pasaron aislados en
segundos. La causa fue mía: solapé tres gates y dos barridos de mutación en la misma máquina.

La medida que lo deja claro: en serie, **123 s**; saturada, **11.780 s** y 18 ficheros en rojo. Un
factor 95 en duración es la señal — antes de leer el nombre del test, mira cuánto tardó.

Consecuencias prácticas:
- **Un rojo de la suite completa aquí no es evidencia de regresión.** Reejecutar aislado ANTES de
  diagnosticar; si pasa en segundos, era hambre de CPU.
- **No solapes gates.** En serie tardan menos y no mienten. Encolarlos con un semáforo (aquí
  `fia-gate`) hace esperar minutos, y eso no es un cuelgue.
- Lo que sí sobrevive a la saturación son `lint`, `typecheck` y `build`: fallan por contenido, no por
  contención. Si esos están verdes y solo la suite baila, sospecha de la máquina.

Vecino, sobre el mismo efecto en la UI: [[cpu-contencion-multisesion-falso-positivo-ui-atascada]].

**Mídelo antes de rediagnosticar, que hay dashboard** (4-sep, facturaia). Un `pre-push` tumbó el
push por UN test rojo; el mismo fichero, solo, dio **9/9 en verde**. `node ~/.claude/gate/gate-dash`
lo dijo sin ambigüedad: `carga 17.2/10 SATURADO`, dos gates ajenos corriendo en otros worktrees. El
orden correcto es dashboard → reejecutar aislado → recién entonces leer el nombre del test. Y la
víctima no fue un test lento: fue un **autotest de un guard estático** que escribe un fichero de
fixture y comprueba que el escáner lo encuentra, con `rmSync` en su `afterEach`. Los tests que tocan
el sistema de ficheros caen por contención igual que los lentos.

Corolario operativo: el hook **hace bien** en bloquear —no se rodea— pero reintentar a ciegas cuesta
otro ciclo entero de 15 min. Se espera a la ventana (`until` sobre carga y workers) y se empuja una
sola vez.

**Y el aislado NO prueba lo que parece.** «Lo corrí solo y da verde» prueba que el fichero está sano
**ahora**; no prueba que el rojo fuera contención. Eso se cierra de una sola forma, y ese mismo día
se hizo: **repetir la corrida COMPLETA que dio el rojo, con menos carga, sin tocar nada**. Antes,
`1 failed | 18353 passed` con la carga en 27; después, `1782 ficheros / 18354 tests` en verde con la
carga en 18. El rojo desaparece al quitar la saturación → reproducir y revertir la condición, que es
prueba, no inferencia. La conjunción «verde en aislado + causa medida» vale como indicio fuerte
mientras tanto, pero no es lo mismo y no conviene confundirlas.

Tres precisiones que sobrevivieron al cierre, y que son el filo de la nota:

- Lo probado es **«el rojo era contención»**, NO «el rojo era tal fichero»: el `| tail` del lanzador se
  había llevado el bloque «Failed Tests» y el nombre no se recuperó nunca. Con dos sesiones señalando
  al mismo candidato el sospechoso es evidente, pero evidente no es medido.
- El **efecto** está medido; el **mecanismo** (I/O y no CPU) es la explicación más probable, no una
  medida. Encaja con que la víctima fuera un autotest de un guard estático —escribe un fixture y hace
  `rmSync` en su `afterEach`— y con que sobreviviera todo lo demás.
- Corolario del pipe: correr con `> fichero 2>&1` **y** `--reporter=json --outputFile=`. Así el nombre
  lo escribe el reporter aunque falles el grep.
