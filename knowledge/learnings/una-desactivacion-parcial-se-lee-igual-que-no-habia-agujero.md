---
title: una desactivación parcial se lee igual que «no había agujero»
date: 2026-08-16
source: claude-code-session
tags: [metodo, testing, mutacion, gates]
---
Para demostrar que un fix arregla algo de verdad hay que medir el ANTES, y la tentación es deshacer
el cambio «a mano» quitando la línea clave. Si la reversión es **parcial**, el resultado es
indistinguible de que el agujero nunca existió.

Caso: tres gates que salían en verde sobre una API sin límite de tasa. Para medir el antes revertí
sólo el recorrido nuevo, dejando arreglada la otra mitad (la clave computada) — y además planté una
trampa con un campo de más que otro gate cazaba por otro camino. Resultado: **2 de 3 saltaron igual**,
o sea «parece que aquí no pasaba nada». Con el fichero entero de `git show HEAD:`, los tres salían 0.

Regla: el «antes» se mide con el **fichero completo tal y como estaba** (`git show HEAD:<ruta>`), y la
trampa que se planta es la **forma exacta** que describe el hallazgo, sin añadir campos.

Es la misma familia que una mutación que dispara por el motivo equivocado: las dos se leen igual desde
el código de salida. Ver [[un-fail-closed-cuenta-la-fuente-que-puede-fallar-no-el-agregado]] ·
[[una-mutacion-que-produce-codigo-valido-no-demuestra-ningun-rojo]].
