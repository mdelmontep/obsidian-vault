---
title: si las observaciones comparten régimen, la muestra efectiva son los periodos, no las filas
date: 2026-07-31
source: claude-code-session
tags: [estadistica, metodo, metricas, verificacion]
---

Calcular el error como `desviación_por_observación / sqrt(n)` asume independencia. Cuando
las observaciones caen dentro de un mismo periodo (trimestre, campaña, release, régimen de
mercado) **no son independientes**, y n exagera la muestra real.

Caso (cryptobruj-bot): con 1.87 de desviación por operación y n=111 salía "veredicto en 3
meses". Pero el walk-forward trimestral daba +0.734, −0.321, −0.071, +0.639, +0.309, −0.122:
la desviación **entre trimestres** era 0.395, cuatro veces el efecto buscado. Con la
dispersión correcta no eran 111 operaciones sino ~5 trimestres — **15 meses, no 3**.

Regla: antes de prometer un plazo, **agrupa por periodo y mira la dispersión entre grupos**.
Si es del orden del efecto que persigues, acumular más filas dentro de un periodo no acerca
la respuesta ni un paso.

Corolario incómodo pero útil: a veces la conclusión es "esto no se puede contestar rápido",
y decirlo vale más que un número bonito. Busca la pregunta *contigua* que sí sea barata — la
determinista, si existe. Ver [[la-pregunta-determinista-se-contesta-con-diez-casos-la-estadistica-con-mil]].
