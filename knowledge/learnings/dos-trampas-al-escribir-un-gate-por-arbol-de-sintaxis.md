---
title: dos trampas al escribir un gate por árbol de sintaxis, y las dos dan el veredicto contrario
date: 2026-08-14
source: claude-code-session
tags: [gates, ast, typescript, harness, tucrmia]
---
Migrar un gate de expresión regular a árbol de sintaxis cierra el alias y el comentario, y abre
dos agujeros nuevos. Los dos vistos el mismo día (TuCRMIA, 14-ago):

**1. Falso VERDE — la clave citada en una referencia de TIPO.** Un gate que pregunta «¿alguien
usa esta entrada del catálogo?» buscando el texto la da por usada aunque el único sitio donde
aparece sea `Database['public']['Enums']['pipeline_stage_kind']`. O sea: **la pantalla rota
citaba la clave con el bug delante**. Hay que exigir llamada o acceso resuelto por LIGADURA, no
coincidencia. Mismo error de categoría que medir un par de contraste que el producto no pinta.

**2. Falso ROJO — comparar posiciones castiga extraer un ayudante.** Si el criterio es «X ocurre
DESPUÉS de Y» por posición del nodo, mover el código a una función declarada arriba lo deja
«antes» y el gate salta **por hacer el trabajo bien**. Un trinquete que se pone rojo al extraer
una función a su sitio se acaba desactivando. Fix: seguir **un nivel** de ayudante local (buscar
la declaración en el ámbito del módulo y mirar las llamadas dentro de su cuerpo).

Regla: prueba el gate **contra el árbol real, no un fixture**, y en los dos sentidos — el falso
rojo sólo aparece al aplicarlo al arreglo correcto.

Ver [[gate-que-valida-por-patron-textual-rechaza-el-equivalente-mas-amplio]] · [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]]
