---
title: gotchas de shell en macOS/BSD — sed no acepta `:label;…;tlabel` en una línea; `while read` se salta la última línea sin \n final; `ps -eo` ignora el `-p`
date: 2026-07-17
updated: 2026-09-07
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

**Tercera (7-sep-2026): `ps -eo … -p <pid>` IGNORA el `-p` y lista todos los
procesos.** El `-e` gana y el filtro no avisa de que no se aplicó. Reproducido:
`ps -eo pid,ppid,command -p 64820` devuelve **576 filas**; sin el `-e`, **2**. El
daño real no es la verbosidad: quien lo remata con `| tail -1` o `| head -1` se
lleva una fila **de otro proceso** con la forma exacta que esperaba, y la lee como
respuesta a su pregunta. Le pasó a una sesión que así concluyó que un gate era de
otra sesión —el ppid que leyó no existía en la respuesta a su pregunta— teniendo en
la misma salida el `cwd` correcto, que contradecía su conclusión. Para un PID
concreto: `ps -o pid,ppid,command -p <pid>`, sin `-e`. Y para saber desde qué
directorio corre algo, `lsof -a -p <pid> -d cwd`, que no admite confusión.

**Y la mitad que generaliza, aportada por la sesión que se lo comió:** el culpable
no fue solo el `-e`, fue **el `| tail -1`**. Sin el recorte habría visto 590 líneas
y habría sabido al instante que algo iba mal — ninguna consulta por un PID concreto
devuelve 590 filas. El recorte no le dio solo la fila equivocada: le **quitó la
única señal** que delataba el fallo. Mismo mordisco que un `| head -6` sobre
`git status`, que cortó justo en la frontera entre trackeados y `??`. Regla:
**un recorte sobre una salida que no has dimensionado antes convierte un error
visible en uno invisible.** Dimensiona primero (`| wc -l`), recorta después.
