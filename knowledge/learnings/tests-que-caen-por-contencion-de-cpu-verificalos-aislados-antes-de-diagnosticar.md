---
title: tests que caen por contención de CPU: verifícalos aislados antes de diagnosticar
date: 2026-07-29
source: claude-code-session
tags: [vitest, testing, verificacion, metodo]
---

Suite completa con 3 ficheros en rojo y ninguno relacionado con el cambio. La
firma de que es contención y no código:

- los tiempos se clavan **en el límite por defecto** (5000-5100 ms en Vitest),
  no en valores dispersos;
- los ficheros caídos no tienen nada que ver entre sí ni con el diff;
- la tanda entera tarda un múltiplo de lo normal (277 s frente a 77 s).

Antes de tocar nada, corre solo esos ficheros: si pasan, era ahogo de CPU
(otro build en paralelo, varias sesiones en la misma máquina), no un fallo.

```bash
npx vitest run <los tres ficheros caídos>
```

No lo des por flaky sin la comprobación aislada: la misma pinta la tiene un test
que depende del orden de ejecución, y ese sí es un fallo real. Lo que distingue
a uno de otro es que el de contención pasa aislado Y la tanda entera vuelve a
pasar cuando la máquina está libre — comprueba las dos.

## Y cuando ya no es la máquina: el tope de fábrica decidiendo el color del rojo (7-ago)

Misma firma —tiempos clavados en el límite, ficheros sin relación— pero **reproducible al
crecer la suite**: 2.609 tests verde 2 de 2; +8 tests y empiezan a caer casos distintos en cada
corrida. Con la máquina a 32 de carga, uno por vuelta; a 15, uno de cada tres.

Si ningún caso de la suite mide cuánto tarda algo, el reloj es sólo el tope para dar por colgado
uno — y con los 5 s de fábrica ese tope lo acaba decidiendo cuántas pestañas tienes abiertas.
Fix: `testTimeout` generoso (20 s) **en un solo sitio**, nunca per-test. No debilita ninguna
aserción: un test roto sigue fallando, sólo que más tarde.

Dos multiplicadores evitables: **mockear un BARRIL** (`vi.mock('@/components/ui', importOriginal)`)
mete los N primitivos dentro de la fábrica del mock —mockea la HOJA—, y los casos que hacen
`await import('@/app/…/page')` transpilan una pantalla Next entera dentro del caso.

Diagnóstico antes de tocar tests: `git stash` (¿flakea sin mis cambios?), sacar los tests nuevos
para aislar, y `uptime`. **Un rojo que se arregla volviendo a lanzar enseña que el rojo es
opinable**, y a partir de ahí nadie mira ninguno.
