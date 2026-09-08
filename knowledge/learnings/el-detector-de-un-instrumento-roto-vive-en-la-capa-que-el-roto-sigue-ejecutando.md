---
title: el detector de un instrumento roto vive en la capa que el roto sigue ejecutando
date: 2026-09-08
source: facturaia
tags: [gates, trinquetes, medicion, metodo]
---
Cuando lo averiado es el propio verificador (un hook viejo, un linter apagado, un
runner que no arranca), **la comprobación no puede ir dentro de él**: si corre la
versión mala, la comprobación nueva no está ahí. Es circular, y da verde.

El criterio para elegir dónde ponerla: **¿qué capa se ejerce pase lo que pase?**
Caso real (facturaia, 8-sep-2026, `core.hooksPath` absoluto): toda versión del
`pre-push`, la vieja incluida, corre la suite de tests. Así que el detector es un
caso de vitest que lee `git config`, no otro bloque del hook — el único sitio con
esa propiedad. El guard dentro del hook se añade igual, pero como **segunda** línea
y diciéndolo por escrito, para que nadie lo tome por el detector.

Segundo criterio, para que el detector no invente su verdad: el valor bueno tiene
**una sola fuente**. Aquí lo declara el `prepare` de `package.json`, y un segundo
caso ata las dos para que no diverjan.

Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]] y
[[una-herramienta-que-se-aplica-a-su-propio-fuente-necesita-el-rescate-fuera]].
