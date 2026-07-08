---
title: un NUL byte literal en un .md hace que git lo trate como binario en diffs
date: 2026-07-08
source: claude-code-session
tags: [git, markdown]
---

Si un archivo `.md` contiene un byte NUL real (`\x00`) —típicamente porque alguien quiso escribir literalmente la secuencia `\x00` en texto y una herramienta lo interpretó como el carácter, no como el string— `git diff`/`git show --stat` empiezan a mostrar `Binary files a/... and b/... differ` para ESE archivo, aunque el resto sea texto normal. El commit se hace bien (el contenido se guarda correcto), pero se pierde el diff legible en PRs/review.

Detectarlo: `python3 -c "print(open('archivo.md','rb').read().count(b'\x00'))"`. Si no fue tu edición la que lo introdujo, no es tu scope arreglarlo — pero vale la pena señalarlo si vas a tocar ese archivo repetidamente.
