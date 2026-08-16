---
title: subir `testTimeout` no toca a `findBy*` ni `waitFor` — su reloj es otro
date: 2026-08-16
source: claude-code-session
tags: [vitest, testing-library, tests, falsos-positivos]
---

Son **dos relojes distintos**. `testTimeout` de vitest es el tope del CASO; las esperas de Testing
Library se rinden con `asyncUtilTimeout`, que vale **1000 ms de fábrica** y no se declara en ningún
sitio. Subir el primero por «fallos bajo carga» —con su comentario explicándolo— no arregla nada si
las esperas son las que se agotan: en TuCRMIA eran **280 (191 `waitFor`, 48 `findByRole`, 39
`findByText`…) en 28 ficheros**, todas con un segundo de margen. Por eso la víctima cambiaba en cada
corrida: no hay «una prueba mala», hay 280 con el mismo margen y cae la que le toque al reparto.

```ts
// src/test-setup.ts
configure({ asyncUtilTimeout: TOPE_DE_ESPERA_MS })
```

Los dos topes, en un módulo con un dueño, y **la espera se rinde ANTES que el caso a propósito**: si
esperan lo mismo, quien corta es vitest y el mensaje es «Test timed out», que no dice nada; rindiéndose
antes, el error lo escribe Testing Library y nombra el elemento que faltaba con el DOM delante.

Subir un tope no debilita ninguna aserción —lo roto sigue rojo, solo que más tarde—, y se comprueba
mutando: esperar un texto que el componente nunca pinta debe seguir fallando (15.017 ms y
`Unable to find an element…`). Ver [[el-control-en-rojo-invalida-cualquier-veredicto-de-mutacion]].
