---
title: un gate que cruza dos listas es ciego a lo que no está en ninguna de las dos
date: 2026-08-10
source: claude-code-session
tags: [gates, arquitectura, testing]
---
Un gate cruzaba la CADENA de comprobaciones contra su TABLA de documentación, en los dos sentidos,
y decía «50 de 50, cada paso tiene su fila» con toda la razón. Dos gates estaban escritos, con test
propio y verdes al ejecutarlos a mano, **y no los ejecutaba nadie**: uno sin entrada en el gestor de
paquetes, otro sin siquiera nombre. Invisibles para el cruce **por construcción**.

El patrón general: cruzar A contra B no ve lo que falta en A **y** en B. Si A y B son dos
representaciones de lo mismo, hace falta una TERCERA fuente independiente — normalmente el disco.

Fix: tercera comprobación contra el sistema de ficheros, con criterio de qué cuenta como gate
(«tiene forma de gate Y tiene test propio»: escribir el test de un gate es declarar que vigila algo)
y lista explícita de los que corren fuera, cada uno con su motivo.

Cuidado al elegir el criterio: la primera versión exigía cadena a TODO script con test y barría
ayudantes y herramientas de mano. Un gate que produce ruido se aprende a saltar.
Ver [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]]
