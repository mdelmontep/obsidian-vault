---
title: una ventana de coordinación entre sesiones se dispara por FICHERO, no por reloj
date: 2026-09-20
source: agh-iberica
tags: [metodo, paralelo, merge, agh]
---
Dos sesiones mergeando el mismo día. La otra pidió *«una ventana de ~20 min sin
mergear a `main`»* porque cada gate suyo de ~6 min se le caducaba antes de terminar:
medía una punta que otro merge ya había movido.

**La ventana por tiempo falla en las dos direcciones a la vez**: bloquea trabajo que
no afecta a quien la pide, y **no bloquea el que sí** — el reloj no sabe qué toca
cada PR. Ella misma lo reformuló: el disparador correcto es *«avísame si vas a
mergear algo que toque `dashboard/web/`»*.

Y ni eso basta, porque **los ficheros que uno toca al CERRAR no son los de su PR**:
mi PR no tocaba `dashboard/web/` pero sí `PROJECT-STATUS.md`, que es justo lo que
ella iba a escribir al cerrar sus issues. El disparador no es un directorio fijo: son
**los ficheros que cada uno va a tocar, incluidos los del cierre**.

La salida no fue «combinar mejor» sino **dejar de escribir a la vez**: primero su
código, luego mi snapshot reconciliado, y ella escribe el suyo **encima del mío ya
mergeado**. Cero conflictos por construcción.

Corolario de reparto, que sirve para decidir sin discutir: cuando dos tocan el mismo
fichero, **uno rebasa sí o sí**, y rebasar caduca también la evidencia cara
(`verify:ui`, evals). Así que la pregunta no es quién tiene prioridad sino **qué
reparto minimiza el trabajo TOTAL** — quien tenga la evidencia cara ya pagada entra
primero. Recomendarlo cuando te perjudica a ti es lo que hace que el otro lo acepte.

Ver [[evidencia-fechada-por-reloj-muere-en-un-rebase]] y
[[una-pr-introduce-el-candado-que-otra-viola]].
