---
title: un guard de texto prohíbe la forma dentro del bloque, no una cadena concreta
date: 2026-09-18
source: facturaia
tags: [testing, gates, metodo, mutacion]
---
Hay invariantes que ninguna prueba de runtime alcanza: el literal de datos dentro de un componente
de 3.000 líneas que nadie monta, o el `select` que el test existente mockea. La cura es un test que
LEE el fichero y asevera sobre su texto, y se escribe mal de dos formas:

- **Prohibir una cadena concreta**: `not.toContain('fecha: isoToDisplay(fecha),')` pasa trivialmente
  si ya no existe, y se pone rojo por una coma de más. Verde sin víctima y falso rojo, a la vez.
- **Buscarla en el fichero entero**: `toMatch(/fecha_operacion/)` da verde porque el identificador
  aparece veinte líneas más abajo, en otra cosa.

Lo que discrimina: **recortar el bloque** (contar llaves desde el literal que vigilas) y prohibir
dentro **la forma** (`/(^|[\s{,])fecha:/`), o citar el tramo exacto del `select`. Se prueba al revés
con `~/.claude/bin/mutate`, con **control negativo**: reordenar columnas es neutro y no debe poner
rojo. Ver [[el-gate-escrito-justo-despues-del-arreglo-mide-cero-casos]] ·
[[un-control-negativo-que-no-discrimina-invalida-el-test-entero]]
