---
title: una aserción de ausencia está verde gratis si el fixture no puede producir la presencia
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [tests, metodo, multi-tenant]
---
Un test que afirma «no pasa X» (sin señal, sin filas ajenas, no propone nada) pasa por
defecto mientras el fixture sea incapaz de producir X. No prueba la propiedad: prueba que
el escenario no ocurrió. Dos formas, las dos en la misma sesión:

- **El camino se abortó antes del guard.** «No marca `commitment_miss` si el batch trae el
  follow-on»: el follow-on no tenía executor en ese arnés y su campo estaba mal → el batch
  se rechazaba entero. La ausencia probaba que **nada se propuso**.
- **El fixture no tiene la fila que delataría la mitad que falta.** Un test de scoping
  poblaba 2 de las 4 celdas (tenant × owner): un `WHERE` que filtrase por tenant y se
  olvidara del owner pasaba igual, porque no existía ninguna fila capaz de aparecer donde
  no debía.

Distinto del fake que hornea la premisa: ahí el doble miente sobre el mundo; aquí el
fixture es honesto pero **incompleto**. Sobrevive a la revisión porque el test se lee
perfecto — dice exactamente lo que quieres que sea verdad.

Fix: (1) toda aserción de ausencia lleva al lado una de que **el camino se recorrió**; (2)
en guards de filtrado, poblar la **matriz entera** y usar `toEqual([lo mío])`, no
`toContain`; (3) verificar rompiendo el guard (quitar el `owner_user_id` del `WHERE`); (4)
si un assert nuevo se pone rojo «donde no debería», sospechar del fixture antes que de ti.
Ver [[test-verde-puede-codificar-el-bug-como-esperado]] · [[regla-en-docstring-no-impide-nada-partir-el-interface]].

**22-ago, la variante del entorno**: un trinquete que afirmaba «no queda ninguna `GIT_*` viva en
`process.env`» pasa sobre un conjunto VACÍO en cualquier shell que no traiga ninguna — verde por no
medir nada (en la mía solo había `GIT_EDITOR`, y de ahí salió el hallazgo). Fix: el `setup` deja
constancia en `globalThis` de que corrió y el test exige las dos cosas. Misma familia, otro caso del
mismo día: un guard que comparaba con `git diff --name-only` ANTES de que existiera el commit no veía
los ficheros sin trackear, o sea que estaba verde sobre lo único que tenía que bloquear.

Formulación corta que cubre las tres: **un guard que puede pasar sin haber examinado nada es verde
por construcción; se prueba con el caso que DEBE bloquear, no con los que deben pasar.**

