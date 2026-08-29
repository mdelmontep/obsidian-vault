---
title: git ls-files miente en las dos direcciones — no ve lo nuevo y sí ve lo borrado
date: 2026-08-06
source: facturaia
tags: [gates, git, ci, static-analysis, tests]
---

Patrón común en gates y tests de análisis estático propio: enumerar el árbol con `git ls-files`
porque es rápido y respeta `.gitignore`. Lista lo **trackeado**, que no es lo que hay en disco, y
eso falla en los dos sentidos:

**No ve lo nuevo.** Un fichero recién creado y sin `git add` no aparece, así que un gate que debería
fallar contra él sale verde **por ausencia, no por corrección** (TuCRMIA, 6-ago: `custom-fields-check.mjs`
daba verde sobre un fichero que sí violaba la regla). Antes de fiarte del verde de un gate nuevo:
`git add` lo nuevo y corre el gate DESPUÉS.

**Sí ve lo borrado.** Una ruta retirada sigue trackeada hasta que el borrado se commitea, así que un
test que hace `readFileSync` sobre cada fila revienta con ENOENT y **tumba la suite entera** por algo
que no tiene que ver con el cambio (FacturaIA, 29-ago: dos barridos de perímetro rojos por dos
endpoints retirados sin commitear). Fíltralo con `existsSync` — no afloja el contrato: una ruta que
no existe no tiene perímetro que defender. Y comprueba que el filtro no vacía el barrido (741
trackeados → 739 existentes, exactamente 2 filtrados).
