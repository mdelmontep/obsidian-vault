---
title: una cota laxa sobre la salida (not.toBe("")) no mide el algoritmo que la produce
date: 2026-09-20
source: agh-iberica
tags: [testing, mutacion, candados, metodo, agh]
---
43 casos en verde sobre la función que calcula el diff de un drift, y **cuatro mutaciones
al núcleo LCS salieron SIN VÍCTIMA**. La causa: las aserciones decían
`expect(salida).not.toBe("")` / `toContain("CREATE")` — cotas sobre la **forma** de la
salida, no sobre su **valor**. Cualquier algoritmo que devuelva algo no vacío las pasa,
incluido uno que alinee mal todas las líneas.

Tiene la cara exacta de un candado: nombre honesto, muchos casos, verde permanente. Lo que
delata es el barrido de mutación, nunca el conteo de tests.

El arreglo son **dos** cosas y hacen falta las dos:
1. **Valor exacto** en los casos pequeños (`toEqual` del string entero, no un `toContain`).
2. Una **propiedad contra un oráculo independiente** para el resto — aquí, una LCS escrita
   aparte en el test. Si los dos la calculan con el mismo código, la propiedad es decorativa.

Regla para revisar: si una aserción **seguiría verde devolviendo una constante plausible**,
no mide el algoritmo, acompaña a su salida.

Ver [[un-candado-derivado-no-se-defiende-de-una-mutacion-de-si-mismo]],
[[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]] y
[[una-asercion-deja-de-medir-cuando-cambia-su-fuente]].
