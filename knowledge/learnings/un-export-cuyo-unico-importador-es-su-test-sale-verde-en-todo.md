---
title: un export cuyo único importador es su propio test sale verde en el arnés, en tsc y en eslint
date: 2026-08-14
source: claude-code-session agh-iberica
tags: [testing, mutacion, cobertura, typescript, metodo]
---
Una función se extrajo a un módulo puro «para sacar la política del sitio difícil», con su test. **Nadie
la importó nunca.** Cinco semanas así, y lo que había en el consumidor era peor que el olvido: **un
comentario** diciendo *«esto lo resuelve `esFantasma`»*, cero apariciones en el bloque de `import`, y
justo debajo **una copia inline de la regla**. El commit que presumía de «política fuera del navegador»
dejó dentro la segunda copia y **escribió que no la había**.

**Por qué no lo caza nada, que es lo que lo hace una clase:**
- **El arnés de mutación le da `✓ VÍCTIMA`** — mutarla rompe *su propio test*, así que confirma
  (correctamente) que la **función** está cubierta. Lo que no existe es el **consumidor**, y eso no lo mide.
- **`tsc` no**: un `export` público sin usar es legal. **eslint tampoco**: `no-unused-vars` no cruza módulos.
- **La revisión humana tampoco**, porque el comentario de al lado afirma que sí se usa.

**Fix:** al extraer una función pura, comprobar con `grep` que el consumidor la **importa**, no que la
menciona — `git log -S "<nombre>," -- <consumidor>` (con la coma del import) distingue import de mención.
Y si el valor de extraer era «que no haya dos copias», la mutación va **en el consumidor**, no en la
función. Ojo al escribir el candado: un export que existe para **inyectarse** (`toString()` en un
`addInitScript`) es legítimo y no aparece como import normal.

Ver [[el-hueco-esta-en-el-cableado-no-en-la-funcion-pura]] · [[una-lista-en-un-comentario-no-protege-el-detector-necesita-una-invariante]]
