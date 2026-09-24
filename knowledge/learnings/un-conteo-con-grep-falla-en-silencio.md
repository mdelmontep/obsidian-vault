---
title: un conteo con grep falla en silencio
date: 2026-09-24
source: facturaia
tags: [medicion, git, shell]
---

Dos ocurrencias, la segunda hoy. **(1)** Un recuento de hallazgos con un patrón mal
construido devolvió 0 y el total exacto en casos distintos: las dos cifras sospechosas
eran el patrón, no el dato. **(2)** Filtrando un diff de git con
`grep -E '^[+-][^+-]'` para ver las líneas cambiadas salieron **cero**, y estuve a
punto de concluir que otra sesión había borrado mi entrada del vault. El patrón
descarta precisamente las líneas de una lista Markdown: `+- 🟠 …` tiene un guion en el
segundo carácter. Lo real era 1 línea cambiada, y nadie había borrado nada.

**Patrón:** un 0 y un «total exacto» son los dos resultados que hay que desconfiar, y
un grep no avisa de que su patrón no case. Se corrobora con una medida de **otra
naturaleza** antes de publicar: `git diff --numstat` (que cuenta sin regex), un
`diff` de blobs, o un hash canónico. En diffs, mejor `--numstat` que filtrar texto.
Ver [[un-diff-de-config-puede-no-tener-ni-un-cambio-semantico]].
