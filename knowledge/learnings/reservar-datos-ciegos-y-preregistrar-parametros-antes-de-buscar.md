---
title: reserva ciega + parámetros pre-registrados: lo único que hace que un hallazgo signifique algo
date: 2026-07-31
source: claude-code-session
tags: [metodo, estadistica, verificacion, tuning]
---

Dos disciplinas baratas que separan un hallazgo de una casualidad, y que hay que montar
**antes** de empezar a buscar:

- **Reserva ciega**: un subconjunto que la búsqueda NUNCA toca (en cryptobruj: dos pares
  enteros + el 30% más reciente de los demás). Se abre **una sola vez**, sobre los
  finalistas. Mirarla repetidamente la convierte en otro set de búsqueda.
- **Contador de intentos**: cada hipótesis probada sube el listón del veredicto (Bonferroni
  sobre el error estándar). Probar más cuesta más, y eso se ve en el número.

Lo que esto atrapó: una variante con **+0.538R** en el set de búsqueda dio **−0.143R** en la
reserva. Era beta de mercado disfrazada de ventaja, y habría pasado cualquier filtro
razonable.

**Pre-registrar** los parámetros (tomarlos de una fuente externa antes de mirar tus datos)
no consume intentos: no hay grados de libertad que explotar. En cuanto alguien pruebe "a ver
si con 12/45 mejora", esa propiedad se pierde — por eso conviene dejarlos **no editables** y
escrito el porqué. Ver [[el-argmax-de-una-mitad-medido-en-la-otra-dice-si-la-superficie-existe]].
