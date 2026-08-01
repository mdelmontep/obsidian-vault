---
title: ante un cast que miente, quitarlo enumera los consumidores; el ?. tapa uno y deja el resto
date: 2026-08-01
source: claude-code-session facturaia
tags: [typescript, type-safety, debug, metodo]
---
Un `x as string` sobre una columna `string | null` no es un atajo de tipos: **desactiva al compilador** como buscador de sitios afectados. Mientras esté puesto, TS no puede señalar ni uno.

Por eso el orden del arreglo importa y no es indiferente: **primero quitar el cast**, y que el compilador liste los consumidores; el `?.` en el sitio donde reventó tapa ESE y deja los demás esperando su turno. En el caso real (qa-037, `/calendario`) el cast ocultaba exactamente dos, y solo uno era el que había crasheado.

Corolario de diagnóstico: el síntoma puede estar a dos saltos de la causa. Aquí la excepción de render desmontaba el árbol, así que el E2E reportaba «no encuentro el botón Hoy» — timeout de 40 s describiendo un botón que existía y luego dejaba de existir. Ante un locator que se esfuma, mirar la **consola del navegador** antes que el DOM.

Y el disparador puede parecer data drift sin serlo: la fila `null` que activó el crash llegó de otro test, pero el bug era de producto y llevaba semanas latente. Data drift como *disparador* no es data drift como *causa*.

Ver [[casts-sobre-data-de-query-supabase-ocultan-42703-que-el-tipo-ya-detecta]] · [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
