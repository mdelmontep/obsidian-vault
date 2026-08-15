---
title: un gate que reconoce una forma por «al menos N claves» se apaga con un spread
date: 2026-08-15
source: claude-code-session
tags: [gates, ast, seguridad, tucrmia]
---
Un gate que identifica «esto es la composición del contrato» contando **claves propias del objeto**
(`suyas.length >= 2`) deja de reconocerla si escribes una sola y traes el resto con `...`:

```ts
const trampa = { ...deps, rateLimit: async () => ({ allowed: true }) }
```

Una clave no llega al umbral → el objeto no se cuenta como composición → **nadie mira su hueco**.
Reproducido sobre el fichero real: la API pública se queda sin límite de tasa y los TRES gates que
cuelgan de ese reconocedor (limitador, plan, dependencias) salen **en verde**.

El umbral no sobra —sin él saltaban 59 objetos de ruta legítimos— pero le faltaba el discriminante:
**ninguno de esos 59 lleva spread**, porque no componen nada. Regla: `N claves` **o** `1 clave + spread`.

⚠️ **Ese arreglo seguía siendo incompleto, y lo encontró la auditoría del mismo día (15-ago, iter. 23):
con CERO claves propias vuelve a apagarse.** `{ ...deps, ...{ rateLimit: relleno } }` no tiene ninguna
propiedad con nombre —un `SpreadAssignment` no lleva `.name`— así que `suyas` queda vacío y no cumple ni
`>=2` ni `>=1 && spread`. Los tres gates otra vez en verde, reproducido sobre `v1.ts`. La regla correcta
no cuenta claves: **si hay spread, es composición, cuente lo que cuente**. Y el comentario que decía
haber cerrado el caso describía sólo la variante de una clave: una cobertura afirmada y no dada es peor
que no afirmar nada.

Patrón general, y es lo que hay que llevarse: cuando un gate reconoce una forma por un UMBRAL, pregunta
qué sintaxis trae lo que falta sin escribirlo — spread, alias de import, desestructuración,
identificador intermedio. Es la misma familia que [[un-import-con-alias-apaga-un-gate-que-busca-texto]].

Y muta contra el fichero REAL: mi primera mutación puso el gate en rojo **por otro motivo** (objeto sin
anotar), así que parecía cubierto. Una mutación que dispara por la razón equivocada se lee igual que un
gate que funciona.
