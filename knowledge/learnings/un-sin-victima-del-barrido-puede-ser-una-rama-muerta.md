---
title: un «sin víctima» del barrido puede ser una rama muerta, no un hueco de test
date: 2026-08-31
source: agh-iberica
tags: [mutacion, tests, metodo, refactor]
---
Un barrido de mutación cierra con «o falta el candado, o el mutante es EQUIVALENTE y hay que declararlo por escrito». **Falta la tercera salida, y suele ser la buena: la rama es inalcanzable y sobra.**

Medido (AGH #1502). Tres `✗ SIN VÍCTIMA` y ninguno era cobertura:
```ts
if (GLUED_DOMAIN.test(first)) { domains.push(first); continue; }
if (!DOMAIN_LABEL.test(first)) continue;
```
`GLUED_DOMAIN` exige al menos un punto y `DOMAIN_LABEL` lo prohíbe: **excluyentes por construcción**. Borrar el `continue` cae en un `if` que siempre rechaza; borrar la guarda deja pasar algo que nunca llega. **Ningún test podía matarlos jamás.** Reescrito como `if/else if` (y `tokens[i+1] ?? ""` en vez de la guarda de `undefined`): **3 → 0 sin añadir un solo test**.

- Ante un SIN VÍCTIMA, antes de escribir el candado o la declaración: **¿es alcanzable el mutante?** Si dos condiciones vecinas son complementarias (una regex que exige lo que la otra prohíbe, un `undefined` ya absorbido por un `??`), la rama sobra.
- **Declarar la equivalencia por escrito la congela**: el comentario envejece y el barrido la vuelve a señalar en cada PR que roce el fichero. Borrar la rama lo cierra para siempre.
- Un candado nuevo sobre una rama muerta es **un test que no puede fallar** — el mismo mal que venías a arreglar.

Ver [[barrer-el-diff-en-vez-de-mutar-a-mano]] · [[al-revisar-muta-la-propiedad-que-la-pr-declara-como-su-aportacion]]
