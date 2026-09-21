---
title: integrar la ola entera antes de mergear caza defectos de composición
date: 2026-09-21
source: agh-iberica
tags: [tren-de-merges, gate, integracion]
---
**Qué pasó:** en un tren de 21 PRs de AGH, todas tenían su gate en verde. Aun así, dos defectos solo aparecían al juntarlas:
- La vista previa daba 500 con los estados que traía el validador de otra PR.
- Un invariante de UI esperaba un selector que el panel nuevo de otra PR había sustituido.

**Patrón por ola:**
1. Crear una rama de integración: `origin/main` más `merge --no-ff` del SHA exacto de cada PR.
2. Correr `verify:ui` y `gate:full` sobre esa rama.
3. Arreglar ahí lo que salga y llevar el arreglo a la PR dueña.
4. Mergear en orden de dependencias con squash, sin `--delete-branch`.

El gate por PR mide cada pieza aislada; la integración mide lo que de verdad va a entrar en `main`.

Relacionado: [[un-fetch-fallido-deja-fetch-head-viejo-y-el-merge-sale-verde]].
