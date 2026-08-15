---
title: reparar datos con la RPC de dominio arrastra sus efectos de negocio
date: 2026-08-15
source: claude-code-session
tags: [migraciones, backfill, dominio, postgres]
---
La tentación al reparar filas mal colocadas es usar la función que ya sabe mover
ese estado («es la única autoridad de transiciones, úsala»). Pero esa función no
mueve un estado: **ejecuta una decisión de negocio**, y trae todo lo que esa
decisión implica.

Caso real (TuFacturaIA, mig 695): devolver dos piezas de `revision` a `guion`
parecía un `marketing_transicionar_pieza(...,'guion')`. Su rama `revision→guion`
es «pedir cambios», así que además habría (1) creado una versión v2 VACÍA,
tirando el guion bueno y obligando a un run del tope diario para reescribirlo, y
(2) guardado el comentario como **regla de estilo del equipo**, que los agentes
leen: una corrección de datos convertida en opinión editorial permanente.

Regla: si lo que arreglas es un dato mal puesto y no una decisión que alguien
tomó, `UPDATE` directo en la migración, con la condición escrita por invariante
y un comentario que diga **por qué se salta la función de dominio**. Si la
función tuviera un modo «sin efectos», usarlo; si no lo tiene, no inventarlo
para un caso único. Ver
[[cambiar-la-ruta-de-una-maquina-de-estados-deja-varadas-las-filas-que-ya-pasaron]].
