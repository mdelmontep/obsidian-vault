---
title: un mutante sin víctima también puede ser un guard equivocado
date: 2026-08-20
source: facturaia
tags: [testing, mutacion, metodo]
---

«SIN VÍCTIMA» se lee siempre como *hueco de test*. Tiene una tercera lectura: **el guard
sobra, o está mal.**

Caso: `if (base <= 0) return null` antes de derivar el % de IVA de base y cuota. Ningún test
lo distinguía de su ausencia, porque el rango `[0,100]` de la canonización ya rechazaba lo
que ese guard pretendía filtrar. Al mirar POR QUÉ era equivalente salió que además estaba
mal: en un abono, base y cuota son las dos negativas y el porcentaje sale correcto, así que
el guard se cargaba justo el caso que había que derivar. Quedó en `base === 0` (la división
imposible) y el signo lo arbitra el rango.

Método: ante un «SIN VÍCTIMA», antes de escribir el test que falta, preguntar qué entrada
distinguiría las dos versiones. Si no existe ninguna, el guard sobra. Si existe y el
comportamiento correcto es el del mutante, el guard estaba mal.
