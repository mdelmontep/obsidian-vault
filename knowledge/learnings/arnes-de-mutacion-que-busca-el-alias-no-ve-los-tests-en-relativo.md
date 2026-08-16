---
title: un arnés que empareja test↔código por el alias no ve los tests que importan en relativo
date: 2026-08-16
source: claude-code-session
tags: [mutacion, tests, arnes, cobertura, falso-positivo]
---

`verify-mutacion` buscaba quién importa un módulo por su alias (`@/lib/foo`). Medido en facturaia:
**621 de 811** ficheros de test importan en **relativo** (`from '../modulos-section'`), así que la
regla fallaba en el **76 %** de los casos y devolvía «SIN TESTS» sobre código bien cubierto.

Se veía así: `modulos-section.tsx` salía con **40 puntos sin tests** teniendo dos ficheros que lo
ejercitan. Tras arreglarlo: **3 muertas, 3 vivas, 0 sin tests** — y las tres vivas eran huecos reales
que el «sin tests» tapaba. Un «sin tests» falso es peor que un superviviente falso: el superviviente
te manda a investigar, el «sin tests» cierra el asunto («ese fichero no está cubierto, normal»).

Dos arreglos, y el segundo se olvida siempre:
- Mirar **las dos formas de importar**, resolviendo el relativo contra el directorio del test: sin
  resolver, dos módulos con el mismo `basename` en carpetas distintas se dan por cubiertos el uno con
  los tests del otro.
- `git grep --untracked`: el gate se corre sobre trabajo **en curso**, y el test que acabas de
  escribir no está en el índice. Sin esto sale «SIN TESTS» justo en la corrida con la que querías
  comprobar que lo cubriste.

Comprobación: coge un fichero con test conocido y mira si el arnés lo empareja. Si dice «sin tests»,
el ciego es el arnés. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
