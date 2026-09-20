---
title: un script que mezcla índice y HEAD se contradice en cuanto hay un rename staged
date: 2026-09-20
source: facturaia
tags: [git, scripts, herramientas, migraciones]
---

`npm run mig:renumerar` falló con `fatal: bad source` sobre un fichero que existía.
La causa no era el fichero: el script calcula el máximo ocupado con `git ls-files`
(que ve el ÍNDICE, con el rename ya hecho) y la lista de migraciones nuevas con
`git diff` contra HEAD (que ve el nombre VIEJO). Con el rename staged y sin commitear,
las dos vistas no describen el mismo árbol y el `git mv` apunta a un origen que ya no
está. Issue #2095 del repo.

- **Fix inmediato**: consolidar el rename en el commit (`git commit --amend`) y volver
  a correr. Idempotente: el segundo pase dijo «ya está en su hueco, no se toca».
- **Patrón general**: dentro de un script, elige UNA vista de git y quédate en ella
  —índice (`ls-files`, `diff --cached`) o árbol de trabajo/HEAD (`diff`, `status`)—.
  Mezclarlas funciona mientras nadie stagee, que es el caso que nunca se prueba.
