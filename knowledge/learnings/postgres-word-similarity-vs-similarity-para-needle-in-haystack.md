---
title: Postgres pg_trgm — word_similarity vs similarity para needle in haystack
date: 2026-05-24
source: TuFacturaIA mig 156 conciliacion fuzzy
tags: [postgres, pg_trgm, fuzzy-matching]
---

# pg_trgm — `word_similarity` vs `similarity` para buscar fragmento en texto largo

Caso: tienes un nombre corto (cliente: "Coca-Cola SL") y quieres saber si aparece en una descripción larga (movimiento bancario: "TRANSFERENCIA COCA COLA SA REF 12345"). La intuición dice usar `similarity(nombre, descripcion)` — está mal.

## La diferencia

- **`similarity(a, b)`**: mide overlap de trigrams de TODA la string A con TODA la string B. Si A es corta y B es larga, el resultado es bajo porque B tiene muchos trigrams que A no.
  - `similarity('coca cola sl', 'TRANSFERENCIA COCA COLA SA REF 12345')` → **0.32**
- **`word_similarity(a, b)`**: mide la mejor coincidencia local de un fragmento de A en cualquier "palabra" o substring de B. Es asimétrico — A es el needle, B es el haystack.
  - `word_similarity('coca cola sl', 'TRANSFERENCIA COCA COLA SA REF 12345')` → **0.82**

## Tabla de calibración real

| Caso | needle | haystack | `similarity` | `word_similarity` |
|---|---|---|---:|---:|
| Match limpio | `coca cola sl` | `TRANSF COCA COLA SA` | 0.32 | **0.82** |
| Sin match | `pepito sl` | `TRANSF SIN CONCEPTO` | 0.04 | **0.10** |
| Match con typo | `cocacola` | `TRANSF COKACOLA SA` | 0.18 | **0.50** |
| Match parcial | `pepito sl` | `TRANSF PEPITO SA` | 0.27 | **0.70** |

`word_similarity` separa correctamente match de no-match.

## Threshold recomendado para conciliación bancaria ES

0.50 con `word_similarity` después de normalizar (lowercase + `unaccent` + alfanumérico):

- < 0.50: aceptaría falsos positivos por palabras genéricas ("sl", "sociedad", "transferencia") que están en muchos clientes y muchas descripciones bancarias.
- ≥ 0.70: perderías typos válidos del banco (COKACOLA, COCACOLLA) y abreviaturas (PEPITO TRANSP en lugar de "Pepito Transportes SL").

Si tras lanzar a producción ves muchos matches rechazados manualmente en rango 0.45–0.55, baja el threshold a 0.45. Si ves auto-confirmaciones falsas, súbelo a 0.55.

## Anti-pattern observado

Confiar en la intuición sin probar — yo puse threshold inicial **0.40** con `similarity()` esperando 0.50+ para casos buenos. Acabé con casos buenos al **0.32**, debajo del umbral. Test rápido en consola SQL evita esto:

```sql
SELECT word_similarity('mi nombre cliente', 'TEXTO DESCRIPCION REAL');
```

Tarda 1 segundo. Define el threshold real.

## Conexión

Va con [[conciliacion-multi-señal-vs-importe-bruto-falsos-positivos]] — el fuzzy es una señal más del scoring, no la única.
