---
title: una PR puede introducir el candado que otra viola — cero solape de ficheros y los dos gates verdes
date: 2026-09-20
source: agh-iberica
tags: [git, merge, gate, ci, metodo, agh]
---
Dos PRs mías, las dos verdes, se habrían matado **en cualquiera de los dos órdenes**:
una añadía un candado nuevo (ninguna línea de `PROJECT-STATUS.md` por encima de 300
code points) y la otra metía trece líneas en ese mismo fichero, tres de ellas de
422, 564 y 518. El candado **no distingue quién escribió la línea**.

Lo caro no es el fallo, es que **los tres instrumentos del tren de merges son ciegos
a esta clase** y los tres dicen la verdad:

- `gh pr diff --name-only` compara ficheros tocados → **cero solape útil** (un fichero
  de `test/` contra nada).
- `mergeable` / `mergeStateStatus` hablan de la mecánica del merge, no del contenido:
  las dos salen limpias, git sabe combinarlas.
- El gate de cada PR corre sobre su rama rebasada: los dos verdes son **ciertos** en
  el instante en que se toman.

La regla del tren de merges está escrita para **contratos de tipos** (dos PRs cambian
la misma cosa). Esto es otra cosa: **una PR introduce la REGLA que la otra viola**.

Y es **asimétrico**, que es lo que lo hace invisible: la PR del candado no necesita
saber que existe la otra, y la del texto no puede saber que va a existir una regla
nueva. Ninguna es culpable, así que no hay a quién preguntarle.

**Por qué no es una anécdota:** un candado es por definición una afirmación sobre
*todo* el fichero o *toda* la carpeta, no sobre las líneas que su PR toca. Así que
**cada PR que añade un candado choca potencialmente con toda PR abierta que toque su
superficie**. Confirmado desde el otro lado por la sesión paralela sin pedírselo: el
candado le impuso la regla a líneas que aún no había escrito.

Detección posible, de más a menos ambiciosa: correr el candado nuevo contra el árbol
de **cada PR abierta**; que el gate diga en su línea «esta PR añade un test que barre
una superficie»; o lo más barato — **mergear los candados AL FINAL del tren**, al
revés que los contratos, para que se midan contra todo lo que ya entró.

Ver [[dos-prs-que-anaden-seccion-al-mismo-doc-conflictan-siempre-apilalos]] y
[[antes-de-tocar-un-ticket-mira-si-otra-sesion-ya-lo-esta-cerrando]].
