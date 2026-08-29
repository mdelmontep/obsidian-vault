---
title: it.each sobre un .filter() vacío no registra ningún test, y vitest no se queja
date: 2026-08-30
source: agentesia-crm
tags: [vitest, testing, guarda-de-cero, falso-verde]
---
`it.each(LISTA.filter(p))(...)` con el filtro devolviendo `[]` **no registra ni un caso** y la suite
sale verde: no hay «0 tests» en ninguna parte, simplemente ese bloque desaparece del recuento total y
nadie mira el total. El día que la forma del dato cambia —otra ruta, otro separador— el cruce se apaga
entero sin que nada lo diga.

**Medido**: mutando el filtro de `catalogo.test.ts` (`'supabase/migrations/'` → algo que no casa) la
suite pasó de **15 casos a 4**, en verde. Con la guarda, falla.

**Fix**: sacar el `.filter()` a una const y añadir un `it` que afirme
`expect(lista.length).toBeGreaterThan(0)` — y, si el universo está partido en dos filtros, que la suma
sea el total. Es la misma [[guarda de cero]] que en gates: un árbol limpio y un recorrido que nadie
hizo imprimen lo mismo si nada los separa. Ver [[un-recorrido-vacio-en-verde-aprueba-cualquier-cosa]].
