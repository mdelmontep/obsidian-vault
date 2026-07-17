---
title: gotchas de shell en macOS/BSD — sed no acepta `:label;…;tlabel` en una línea; `while read` se salta la última línea sin \n final
date: 2026-07-17
source: claude-code-session
tags: [bash, sed, macos, scripting]
---
Dos que costó depurar en scripts bash portables (macOS/BSD):

1. BSD `sed` NO admite label+comando+branch en una sola línea con `;`: `sed -E ':a; s/…//; ta'` da `unused label 'a; s/…'` y (con `pipefail`) revienta el pipeline entero en silencio. Para "repetir hasta que no matchee" usa un grupo `(...)+` en una sola sustitución, sin loop de label: `sed -E 's/^([A-Za-z_][A-Za-z0-9_]*=[^ ]* +)+//'`. (Al contrario de la creencia común, `\n` en el *replacement* SÍ funciona en el BSD sed moderno de macOS.)

2. `while IFS= read -r x; do …; done < <(cmd)` OMITE la última línea si la entrada no acaba en `\n` (típico de `printf '%s'` o `sed` sin newline final). Síntoma: "el último elemento troceado desaparece". Fix: `while IFS= read -r x || [ -n "$x" ]; do`.

Ver [[fia-gate]].
