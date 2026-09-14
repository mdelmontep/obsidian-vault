---
title: una migración con excepciones verifica las dos mitades, o el uuid mal tecleado sale verde
date: 2026-09-14
source: claude-code-session facturaia
tags: [migraciones, sql, postgres, verificacion, gates]
---

Migración que apaga una concesión a todos **salvo** a una lista nominal de orgs. Su
autoverificación contaba lo obvio: «que no quede ninguna organización real encendida».

Ese predicado solo sabe contar **lo que NO debería quedar**. Con un uuid mal tecleado
la excepción no protege a nadie, la concesión se apaga también para ella, y el recuento
de «los que sobran» sigue siendo cero: verde. El fallo que la migración venía a evitar
es indistinguible del éxito.

- **Mide las dos mitades**: nadie de más, y `count(exceptuados con la concesión viva) = count(lista)`.
- **Declara la lista una sola vez**: `CREATE TEMP TABLE … ON COMMIT DROP` que leen el
  `UPDATE` y la comprobación. Dos copias acaban diciendo cosas distintas y la migración
  se autoaprueba contra el predicado equivocado. Sin residuo: `db push` corre cada
  fichero en su transacción (10 migraciones ya en prod lo usan).

Misma familia que [[un-registro-de-ultima-corrida-cuenta-verde-lo-que-nunca-pregunto-si-paso]]:
un gate de una sola dirección no distingue «funcionó» de «no llegó a correr».
