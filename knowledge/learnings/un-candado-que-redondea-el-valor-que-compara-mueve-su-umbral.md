---
title: un candado que redondea el valor que compara mueve su umbral
date: 2026-08-05
source: claude-code-session
tags: [testing, qa, metodo, accesibilidad, verificacion]
---
Si un test compara una **medida** contra un **umbral**, redondear el valor comparado no es cosmético:
**mueve el umbral**. El redondeo entra siempre con buena intención («que el mensaje se lea») y en el
sitio peor: la función que calcula, que es la que decide.

Caso real (agh-iberica #881): `ratioContraste` acababa en `Number(x.toFixed(2))`, así que
`--orange-700`/`--orange-100` a **4,4975:1** (incumple AA) pasaba como `4.50`. El test **declaraba
ese par**, con suelo y aserción correctos, y llevaba semanas aprobando el incumplimiento — regalando
±0,005 a los **23** pares.

- Redondear **solo al formatear el mensaje**, nunca en el valor que entra al `expect`. Dos funciones.
- Dar decimales suficientes para ver el filo: `4.4975` cuenta otra historia que `4.50`.
- **Trampa: arreglar el dato hace el redondeo indetectable** — «sin víctima» que no es equivalencia,
  es que ya no queda dato en el filo. Se cierra con un test del **helper** cuyo fixture sea el dato
  viejo. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
- Recalcular la tabla del issue por tu cuenta: aquí sacó que **7 de 23** pares viven a <0,05 del suelo
  — no cambia el arreglo, cambia la lectura del riesgo.
- Si piden «captura antes/después» de un color, hay métrica: **ΔE2000 contra el JND (≈1)**. 0,3965 =
  imperceptible **medido**, y no depende de tu ojo.
