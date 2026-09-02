---
title: gotchas de shell en macOS/BSD — sed no acepta `:label;…;tlabel` en una línea; `while read` se salta la última línea sin \n final
date: 2026-07-17
updated: 2026-09-02
source: claude-code-session
tags: [bash, sed, macos, scripting]
---
Dos que costó depurar en scripts bash portables (macOS/BSD):

1. BSD `sed` NO admite label+comando+branch en una sola línea con `;`: `sed -E ':a; s/…//; ta'` da `unused label 'a; s/…'` y (con `pipefail`) revienta el pipeline entero en silencio. Para "repetir hasta que no matchee" usa un grupo `(...)+` en una sola sustitución, sin loop de label: `sed -E 's/^([A-Za-z_][A-Za-z0-9_]*=[^ ]* +)+//'`. (Al contrario de la creencia común, `\n` en el *replacement* SÍ funciona en el BSD sed moderno de macOS.)

2. `while IFS= read -r x; do …; done < <(cmd)` OMITE la última línea si la entrada no acaba en `\n` (típico de `printf '%s'` o `sed` sin newline final). Síntoma: "el último elemento troceado desaparece". Fix: `while IFS= read -r x || [ -n "$x" ]; do`.

3. **BSD `sed` no conoce `\b`** (frontera de palabra: es una extensión GNU). `sed -E 's/\bmig 793\b/mig 795/g'`
   no da error, no avisa y **sustituye cero veces**, con exit code 0. Es el peor de los tres: los otros
   dos revientan, éste te deja creyendo que renumeraste 52 referencias cuando no tocaste ninguna (2-sep,
   facturaia #2379, barrido de `mig NNN` en 34 ficheros). En BSD la frontera se escribe `[[:<:]]`/`[[:>:]]`,
   pero para un barrido con recuento **usa Python**: `re.subn` devuelve cuántas veces sustituyó por fichero,
   y ese número es la única prueba de que el barrido hizo algo.

**Lo transversal**: en `sed` el exit code mide «hubo entrada que procesar», no «cambié algo». Cualquier
sustitución masiva se verifica volviendo a grepear el patrón viejo en todo el árbol, nunca por su `$?`.

Ver [[fia-gate]] · [[colision-de-numero-de-migracion-hace-que-db-push-la-salte-en-silencio]].
