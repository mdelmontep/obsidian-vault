---
title: antes de tocar un ticket, mira si otra sesión ya lo está cerrando
date: 2026-07-28
source: claude-code-session
tags: [metodo, git, sesiones-paralelas, facturaia]
---

Con varias sesiones abiertas sobre el mismo repo, el ticket o el issue **no sabe**
que otro ya lo está atacando. Comprobación de 5 segundos antes de escribir nada:

```
gh pr list --state all --search "<palabra del área>"
git log origin/main --oneline -20
```

Dos ocurrencias el mismo día (2026-07-28), la segunda con la lección ya escrita:
- Suite smoke E2E: dos ramas diagnosticaron por separado los mismos dos hallazgos.
- Ticket #86 (retención): el #1296 arreglaba la ficha mientras yo hacía el listado.
  Se vio al mergear, en forma de conflicto, no antes.

Lo caro no es el trabajo repetido, es lo que casi pasa: un cambio mío rompía una
aserción verde ajena, y en el segundo caso las dos ramas tocaban las mismas líneas
de un cálculo de importes. **Resolver un conflicto así no es elegir un lado**: hay
que leer QUÉ intentaba el otro y quedarse las dos mitades, porque suelen ser
complementarias (allí: su copy de usuario + mi fuente única del número).

Y al resolver, grep de las referencias por número de línea (`fichero.tsx:799`) que
el otro haya dejado en comentarios: si tu rama mueve esa línea, quedan mintiendo.

Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] ·
[[comentario-que-declara-una-formula-deliberada-solo-cubre-su-mitad]]
