---
title: un gate de «está enchufado» no se copia entre huecos que se rellenan de forma distinta
date: 2026-08-11
source: claude-code-session
tags: [harness, gates, ast, arquitectura, tucrmia]
---
Un objeto de dependencias (`Deps`) con N huecos que un doble puede rellenar sin que nada se
ponga rojo — ningún test lo caza, porque el doble que inyecta cualquier prueba **es** un literal.
La tentación al escribir el gate del hueco 3 es copiar el del hueco 1. No vale: depende de CÓMO
se rellena cada uno, y el criterio equivocado suspende trabajo correcto (P5 → se desactiva).

- **Lo rellena una fábrica importada de otro módulo** → el criterio es la **procedencia**:
  `vieneDe(ligaduraDe(raiz), '@/core/x')`. Contesta la pregunta entera.
- **Se escribe en el propio módulo de composición** (el único que sabe de la base) → procedencia
  no vale: los suspendería a todos. El criterio es **alcanzar la E/S**: recorrer el subárbol del
  hueco y exigir una llamada cuya raíz se resuelva a un import de la puerta al mundo
  (cliente de BD, HTTP saliente). `log: async () => {}` es idéntico en forma a un puerto que
  funciona; lo que no tiene es una sola llamada a la base.

Resolver por **ligadura, no por nombre**: el cliente suele importarse con alias
(`clienteDeServicio as getClient`) y un homónimo local no es la puerta. Y seguir tanto `const`
como `function foo()`, o el gate suspende una mitad del puerto por cómo está declarada.
Demostrar el rojo **sobre el árbol real**, no sobre fixtures. Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]].
