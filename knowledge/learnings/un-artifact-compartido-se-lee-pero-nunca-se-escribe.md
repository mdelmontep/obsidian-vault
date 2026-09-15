---
title: un artifact compartido se lee pero nunca se escribe, y recrearlo cuesta lo que lo cite
date: 2026-09-15
source: agh-iberica
tags: [artifacts, claude-code, harness, coordinacion]
---
Un tablero de progreso vivía en un artifact de otra cuenta. Desde esta sesión se puede
LEER y nunca escribir: solo la cuenta propietaria publica versiones. El discriminador
barato, antes de culpar al acceso: `action:"list"` funcionó y devolvió 24 artifacts, y el
tablero no estaba entre ellos → no es el permiso de artifacts, es ese tablero.

Recrearlo no es gratis: la copia nace con URL nueva, y el coste real es **todo lo que
cite la vieja** (aquí, 19 issues de GitHub; en el repo, cero apariciones — hay que contar
las dos cosas antes de decidir).

Consecuencia de diseño: un tablero que varias sesiones deben actualizar no se pone en la
cuenta de una persona. O vive donde todas escriben (issue, fichero del repo), o se acepta
que solo su dueña lo mueve y el resto entrega el delta medido.

Ver [[el-canal-obligatorio-caido-deja-el-ciclo-sin-cerrar]].
