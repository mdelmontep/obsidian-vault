---
title: es-es no agrupa los millares de 4 cifras — no es icu roto, es la regla
date: 2026-06-22
source: claude-code-session
tags: [testing, vitest, intl, i18n]
---
`new Intl.NumberFormat('es-ES').format(1250)` da **"1250"**, no "1.250". Igual en
currency ("1250,00 €") y **igual en el navegador**: medido 13-ago con ICU 78.3
completo. Agrupa a partir de CINCO cifras (18200 → "18.200"), que es la
convención tipográfica española recogida en CLDR, no un build sin `full-icu`.

Esta nota culpaba antes a "Node ICU sin full-icu". Era falso, y una causa falsa
manda al siguiente a instalar `full-icu` para arreglar algo que no está roto.

Coste real: un test aseveraba `/1\.820 facturas/` y salía rojo con el componente
correcto (facturaia #1699). Se arregló el test, no el formateo.

Fix: en tests, no aseverar el string formateado completo. Aseverar el dato crudo
(`expect(item.count).toBe(1250)`) y, como mucho, el símbolo (`toMatch(/€/)`).
Si necesitas el string, genéralo con el mismo `Intl` en vez de teclearlo.
