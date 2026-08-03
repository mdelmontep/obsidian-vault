---
title: un gate que lee por regex también lee los comentarios, y falla en las dos direcciones
date: 2026-08-03
source: claude-code-session
tags: [tooling, ratchets, linters, hooks, gates]
---

Un gate que busca en el **texto** y no en el AST cuenta lo que hay en los comentarios. Falla en
las dos direcciones, y la segunda es la peligrosa:

- **Falso positivo (benigno, bloquea).** Un trinquete que cuenta `style={{`, `<button` o hex
  crudos sube el contador con un comentario que **cita** el patrón prohibido: explicar por
  escrito que lo evitaste rompe el commit. Suele fallar cuando la línea no **empieza** por `//`.
- **Falso negativo (mudo, deja pasar).** Un gate que exige que una migración revoque `EXECUTE`
  daba por buena una función `security definer` cuyo `revoke` estaba **comentado**, o citado
  como ejemplo en la prosa de cabecera: `EXECUTE` a `PUBLIC` con el gate en verde. Esta
  dirección no molesta a nadie, así que nadie la mira.

- **La variante más vil (3-ago): el comentario que EXPLICA la regla la satisface.** Un gate nuevo
  comprobaba que la app escribiera `data-theme`; al mutar el layout para enseñar el rojo **siguió
  verde**, porque el comentario recién escrito para justificar el atributo contiene la palabra
  `data-theme`. Sin correr la mutación se commitea como protección. En TS/TSX hay que escanear
  respetando cadenas: distinguir el `//` de `'https://…'` del que abre comentario no lo hace una
  regex.

**La regla: dos pasadas.** Sin comentarios para buscar SENTENCIAS; en crudo para buscar
MARCADORES (`rls-regime:`, `rls-helper`, `token-entrada:`, `selector-entrada:`), que viven dentro
de un comentario a propósito. Quitarlos a secas arregla un lado y rompe el otro.

Y al escribir el comentario: describe el patrón prohibido, no lo cites literalmente.

Ver [[un-detector-que-enumera-sintaxis-se-queda-corto-comprueba-la-identidad]] ·
[[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]] ·
[[reglas-duras-en-prosa-acaban-en-hook]]
