---
title: «la tabla existe y nadie le escribe» no es lo mismo que «no existe», y el candado se queda corto
date: 2026-08-15
source: claude-code-session
tags: [observabilidad, gates, diseño, tucrmia]
---
Un panel declaraba qué bloques **no puede enseñar todavía**, cada uno con su tabla, y su candado
era «si esa tabla ya existe en los tipos, la entrada sobra». Al aplicar la migración, el candado
pidió borrarla — y las dos salidas eran mentira:

- **Borrar la entrada** quita el bloque de la pantalla *sin declarar el hueco*. Un bloque que
  desaparece se lee igual que uno que nunca existió.
- **Construirlo** pinta un cero sobre una tabla **sin productor** (su escritor llega en la
  entrega siguiente). Y ese cero era la señal con la que se decide escalar infraestructura.

Fix: la espera tiene **dos formas**, cada una con su comprobación ejecutable — `tabla` (no está
en los tipos) y `emisor` (está, y nadie de `src/` le escribe, buscado en el árbol y no en una
lista a mano). Es la familia de G-CAT / G-USO-EMISOR aplicada a una pantalla: **una columna que
siempre vale cero se lee igual que «esto no pasa nunca»**.

Regla general: cuando un candado te pida borrar una declaración, comprueba si lo que cambió es
la condición que declaraba o **sólo una de sus mitades**.

Ver [[consumidor-lee-claves-que-productor-no-emite]] · [[un-detector-nuevo-cuyo-cero-no-mediste-antes-no-vale]]
