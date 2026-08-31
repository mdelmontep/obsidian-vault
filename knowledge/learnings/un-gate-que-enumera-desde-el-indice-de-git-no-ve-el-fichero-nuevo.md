---
title: un gate que enumera desde el índice de git no ve el fichero que acabas de crear
date: 2026-09-01
source: facturaia
tags: [gate, git, testing, hooks, rutas]
---

`escrituras-sesion-parametro.test.ts` exige que toda ruta de API con un segundo parámetro dinámico declare su resolver de permisos. Enumera las rutas **desde el índice de git**, no desde el disco. Así que una ruta recién creada y aún sin `git add` **no existe** para él.

Consecuencia práctica, y es al revés de lo que uno espera: **el gate local dio EC=0 sobre exactamente lo que el `pre-push` rechazó después**. Corrí `npm run gate` con el fichero untracked (verde: la ruta era invisible), commiteé, y el `pre-push` — que corre la misma suite pero ya con el fichero en el índice — la vio y la marcó «sin recurso». El fallo aparece **después** del commit, cuando ya no puedes decir «el gate estaba verde».

Regla: si el repo tiene candados que enumeran ficheros versionados (rutas, migraciones, exports), **`git add` antes de correr el gate**, no después. Un `git status` con `??` sobre un fichero del área que el candado vigila es la señal.

Y el otro lado: enumerar del índice es la decisión CORRECTA para un candado de esta clase (mide lo que se va a mergear, no el barro local). Lo que falta no es cambiar la fuente, es no fiarse de un verde obtenido con el árbol sucio.

Ver [[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]] · [[mover-un-fichero-rompe-todo-gate-indexado-por-ruta]]
