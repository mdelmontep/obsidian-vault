---
title: el hueco de test suele estar en el cableado, no en la función pura que el issue nombraba
date: 2026-08-12
source: claude-code-session agh-iberica
tags: [testing, mutacion, diseno, metodo]
---
Tres veces en una sola tanda (AGH, familia `mutate:diff`): el issue pedía arreglar una **lógica**, la
lógica quedó cubierta, y la mutación destapó que el hueco real estaba en el **punto de unión**, dentro
de un `main()` que ningún test invoca.

El caso tipo: `anotarEnDiario(…, mutante)` y `writeFileSync(ruta, mutante)` como dos llamadas sueltas.
Pasar ahí el argumento equivocado **sobrevive a la suite entera** — y el efecto no era cosmético (el
diario dejaba de restituir *nunca*). El diff se lee perfecto: cada llamada es correcta por separado;
lo que está mal es que **la pareja se puede desparejar**. Eso no se ve leyendo, solo mutando el punto
de unión — no la lógica que el issue nombraba.

**El arreglo bueno no es otro test: es colapsar la pareja en un valor** que fluye (una función que
hace las dos cosas; o devolver `{a, b}` y que el consumidor lo tome entero en vez de dos parámetros).
Así el defecto es **inexpresable**. Mismo principio que derivar una whitelist de un `Record<Union,
true>` en vez de escribirla a mano.

Si el cableado no se puede cubrir porque el `main()` no es invocable: **declara en el código qué
mutación sobrevive**, con qué se cubre en su lugar (una corrida real **con contrafáctico**), y abre
issue — dejarlo en la PR no lo pone en ninguna cola.

Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
