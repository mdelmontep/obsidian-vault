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

Tercera ocurrencia (2026-07-29, anchos de columna): la señal NO fue un PR abierto
—no lo había— sino **cambios sin commitear en el checkout raíz sobre mis mismos
ficheros**, que solo aparecieron al fallar el `git pull` con "your local changes
would be overwritten". Añade `git status` del checkout compartido a la
comprobación de 5 segundos. Las dos ramas llegaron a la misma solución CSS por
separado; mientras yo fusionaba, el otro mergeó lo suyo (#1338) y mi PR de
fusión (#1337) nació redundante y se cerró. Antes de cerrarlo: verificar que lo
que quedó en main es coherente (allí, que ninguna mitad dejara una clase
referenciada pero inexistente).

Ver [[claude-code-sesiones-paralelas-mismo-repo-colisiones-git]] ·
[[comentario-que-declara-una-formula-deliberada-solo-cubre-su-mitad]]

**Reincidencia 2026-07-29, y no era un ticket sino un ÁREA**: en la misma
mañana, dos sesiones arreglaron por separado el mismo bug de anchos de columna
en Materiales (mismo diagnóstico, misma solución `width: 0` + spacer) y otras
dos implementaron la misma columna fija. Coste: un PR cerrado por duplicado
(#1337), una rama rehecha desde cero y trabajo tirado. La comprobación vale
igual para un área de código, no solo para un ticket con número:

```
gh pr list --state open | grep -i "<área>"
git log origin/main --oneline -10 -- <ruta del área>
```

Y el disparador no es "voy a cerrar un issue", es **"voy a tocar estos
ficheros"**.
