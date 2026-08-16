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

⚠️ **CERRADO EL 16-AGO (iter. 25), y la forma final importa.** El arreglo de aquella mañana seguía
siendo incompleto: `{ ...deps, ...{ rateLimit: relleno } }` no tiene ninguna
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

**El arreglo NO es «si hay derrame, cuenta»** —eso daría por composición cualquier `{ ...algo }` del
árbol, y un gate que falla sobre trabajo correcto es el que alguien acaba apagando—. Lo que discrimina
es que **las claves del derrame tienen nombre cuando lo derramado es un literal escrito ahí mismo**:
se abre ese literal, recursivamente. Lo que no se puede saber —qué trae `...deps`, que es otro
fichero— sigue sin saberse. El umbral no cambia; cambia qué cuenta como clave. Y de paso entró la
clave computada con literal de cadena (`{ ['rateLimit']: … }`), que tampoco resolvía por nombre.

Medido sobre el fichero real con `git show HEAD:`: antes los tres gates con salida **0**, después
los tres con **1**. Ver [[una-desactivacion-parcial-se-lee-igual-que-no-habia-agujero]].
