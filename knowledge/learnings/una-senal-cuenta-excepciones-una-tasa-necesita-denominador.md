---
title: una señal cuenta excepciones; si quieres una tasa, necesitas la dimensión
date: 2026-08-05
source: claude-code-session
tags: [observabilidad, medicion, evals, telemetria]
---

Antes de escribir «esto no se puede medir», **enumerar la taxonomía cerrada que ya existe** (el enum, el union type, la tabla de razones) y leer el comentario de cada valor: suelen declarar qué se decidió NO medir y por qué, y ese rationale es media issue.

Caso AGH (5-ago): afirmé que el 32,8 % de `clarify` no se podía partir por causa. **Ya se partía** — `kind:"asked"` con ocho razones, cada una con un test que ejercita su camino. Peor: la respuesta estaba escrita en mi propio hub del vault desde el 1-ago («agregaba 4 conductas y excluía 5 caminos»).

**El error de forma, que es el reutilizable:** iba a añadir una señal de *miss* cuando lo que faltaba era una **dimensión por turno**. Una señal se emite en la excepción → da numerador. Una tasa necesita el denominador, o sea una propiedad de **todos** los eventos (en AGH, el patrón de `intent`/`readTarget`). Numerador sin denominador es exactamente cómo un agregado se traga una regresión real.

Y si el repo ya rechazó por escrito mezclar dos cosas en una métrica, añadir tu señal al mismo evento que ya emite otra **es** esa mezcla.

Corolario de egress: el valor de una dimensión sale de un conjunto cerrado calculado por tu código, nunca de texto del modelo o del usuario — si no, la telemetría se convierte en canal de contenido. Ver [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]].

Hermanos: [[el-verde-de-evals-check-no-significa-que-nada-se-movio]] · [[senal-de-capacidad-ausente-que-solo-ve-el-target-inventado]]
