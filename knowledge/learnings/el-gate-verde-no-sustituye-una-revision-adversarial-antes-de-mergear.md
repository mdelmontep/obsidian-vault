---
title: el gate verde no sustituye una revisión adversarial antes de mergear
date: 2026-07-29
source: claude-code-session
tags: [metodo, testing, subagentes, revision]
---
Un gate verde solo dice que **los tests que escribiste** pasan. Si el test comparte con el código la premisa equivocada, el verde es cosmético: mide la forma del fake, no el comportamiento.

Caso real (agh-iberica #585, 29-jul): fix implementado, 5 tests verdes, gate `2043/203/3` limpio. Tres subagentes con lentes DISPARES —correctitud, integración/regresión, producto+RGPD— lanzados **antes** de abrir la PR. Dos llegaron por su cuenta al mismo bloqueante: el guard no habría casado nunca en producción ([[graph-devuelve-la-hora-del-evento-como-pared-sin-offset]]). Los otros hallazgos (falsos positivos por `includes`, ventana fija que anulaba el guard a 45 días, llamada de red sin tope dentro del camino del turno) también eran reales.

Reglas que funcionan:
- **Lentes distintas, no tres veces la misma**: la coincidencia de dos revisores independientes en el mismo punto es la señal más fuerte que vas a tener.
- **Pedir escenario concreto** por hallazgo («inputs → resultado incorrecto») y decir explícitamente «prefiero 2 hallazgos ciertos que 10 especulativos»: sin eso, ~50% son falsos positivos.
- **Verificar cada hallazgo tú** antes de tocar código. Aquí se comprobó la TZ del contenedor de prod, no se dio por buena la afirmación.
- Va **antes** de la PR, no después de mergear: después ya es un incidente.

Ver [[audits-cross-pr-vs-per-pr]] · [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]].

**Y funciona igual —o mejor— sobre tus PROPIAS PRs, con una instrucción distinta** (agh, 5-ago, tres
PRs mías): no «revisa esto» sino **«ataca mis afirmaciones y recalcula mis números»**. Lo que cazó y yo
no: dos **errores de contabilidad** en la descripción («7 de los 15» cuando eran nueve — y el número
sostenía mi argumento); una **copia ambigua** que en el caso de su propio golden mandaba al usuario a
buscar en el sitio equivocado; **dos ratios de fixture medidos a ojo** en una PR cuya tesis era «no
aproximes». Y confirmó midiendo un flake que yo temía sin datos (10/10 con la CPU al 92 %). Dos
detalles que lo hacen rendir: pedirle que **recalcule desde cero** lo que la PR afirma (aquí, la
fórmula WCAG entera) en vez de leer mis cifras, y decirle **qué NO entra** para que no arregle nada.

**Corolario que salió de ahí:** una **magnitud** escrita a ojo cuesta lo mismo de medir que de
afirmar. Escribí «alinear el fake toca todos los tests de brain»; eran **6** — y al medirlo apareció el
hallazgo de verdad, que esos 6 protegían un estado que una migración ya hace **imposible**.
