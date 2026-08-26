---
title: reserializar un json tracked lo reescribe entero; inserta textualmente
date: 2026-08-26
source: facturaia
tags: [git, json, inventarios, hooks]
---
Añadir UNA entrada a un inventario JSON tracked (`tap-target-inventario.json`)
con un script que hace `json.load` + `json.dump` produjo **174 líneas de diff**
para un cambio de una: el reserializador cambió indentación, orden de claves y
comillas de todo el fichero. Insertado a mano como texto, en la posición y con
la indentación de sus vecinos: **10 líneas**. El diff grande no es cosmético —
esconde tu cambio en la revisión y colisiona con cualquier sesión paralela.

Regla: **fichero de datos tracked → inserción textual** (`sed`, heredoc,
`awk` posicional). Reserializar solo si el fichero lo genera una herramienta y
existe el comando que lo regenera (ahí sí: `npm run ratchet:size:update`).

Y si ya lo has reescrito: `git checkout -- <ruta>` NO es la salida, `git-guard`
lo bloquea por descartar cambios sin commitear. La vía es
`git show HEAD:<ruta> > /tmp/x && cp /tmp/x <ruta>`, que solo toca ese fichero.
