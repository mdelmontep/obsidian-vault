---
title: un identificador que no casa tiene que vetar el respaldo por nombre, no solo perder prioridad
date: 2026-07-31
source: claude-code-session
tags: [matching, dedup, datos, fiscal, ocr]
---
Tres implementaciones del mismo emparejado de proveedores decían por comentario que el NIF era la
identidad fuerte y el nombre el respaldo. **Ninguna lo cumplía.** El patrón era siempre el mismo:

```
byNif ?? byNombre          // TS
IF FOUND THEN RETURN; END IF; -- ...y si no, sigue buscando por nombre, alias y fuzzy
```

Eso no es "el NIF tiene prioridad", es "si el NIF no casa, da igual el NIF". Un documento con NIF
`B12345674` acababa colgado de una empresa con NIF `A78875499` porque el nombre coincidía. Medido en
producción, y aquí va la segunda lección: la primera consulta dijo **92 facturas** y **no agrupaba por
organización**, así que mezclaba la sandbox de pruebas con los clientes. Separando `is_test`, eran 8 en
clientes reales y solo **2** atribuciones a otra empresa. Un alcance inflado 11 veces dimensiona mal el
trabajo y quema la credibilidad del resto del informe. Aun así, cada una de esas 2 es una línea del 303
y del 347 con el NIF de un tercero, y el 347 lo declaran las dos partes.

Reglas:
- Identificador informado que **no** casa → no se empareja. Punto. Solo se acepta el respaldo por
  nombre contra un candidato **sin** identificador, que no contradice nada.
- Normaliza el identificador en TODAS las capas o abres la misma puerta: `upper(trim())` en SQL
  frente a quitar puntuación en TS deja que un `B-12.345.674` ni intente el match y caiga al nombre.
- **Escribir de vuelta el nombre observado como alias convierte un enlace erróneo en permanente**:
  a partir de ahí acierta "de libro" y ningún identificador lo desmonta. Solo aliasear si el
  identificador no contradice. Caso real: FacturaIA `qa-023`, `resolve_proveedor`.
