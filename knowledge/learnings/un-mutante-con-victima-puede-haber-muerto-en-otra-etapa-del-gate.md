---
title: un mutante con víctima puede haber muerto en otra etapa del gate
date: 2026-09-05
source: mandadm
tags: [mutacion, testing, arnes, metodo]
---
Quitar una función para comprobar que un test la protege deja su `import` huérfano: el gate se pone
rojo en **lint**, no en el test. El arnés informa «CON VÍCTIMA» y no miente, pero **mide otra cosa** —
el test podría no tener dientes y no lo sabrías.

Es el inverso de los «sin víctima» falsos ya conocidos ([[el-barrido-que-salta-los-tests-relevantes-dice-sin-victima]],
[[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]]): allí el arnés no mide, aquí mide de más.

**Fix, dos mitades:**
- Que el gate diga **en qué etapa** murió. `scripts/gate.sh` imprime una línea `a b c d` con el exit de
  lint / typecheck / build / vitest; el mutante solo vale si el que se pone a 1 es el cuarto **y** el
  fallo es la aserción que esperabas, con su fichero:línea. Leerla en cada mutación, no solo el rojo.
- Elegir mutaciones que **no rompan la compilación**: cambiar el VALOR que se compara, no borrar el
  símbolo. `'Tecnocloud'` → `'{{PROVEEDOR_HOSTING}}'` mata el test y deja el resto del gate verde.
