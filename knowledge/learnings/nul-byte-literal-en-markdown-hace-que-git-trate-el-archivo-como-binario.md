---
title: un NUL byte literal hace que git, grep y file traten el fichero como binario
date: 2026-07-08
updated: 2026-07-31
source: claude-code-session
tags: [git, grep, markdown, typescript, debugging]
---

Un byte NUL real (`\x00`) en un fichero de texto lo vuelve **binario** para las
herramientas de línea. Suele colarse al querer escribir la secuencia `\x00` y que
algo la interprete como el carácter (ver [[write-tool-byte-nulo-en-template-literal]]).

- **git**: `git diff`/`show --stat` dicen `Binary files … differ`. El commit se
  guarda bien; lo que se pierde es el diff legible en la PR.
- **grep** (31-jul, AGH, 3 fuentes `.ts`/`.tsx`): sin `-a` devuelve **cero
  coincidencias con exit 1** — no un aviso, un «no está». Casi se concluye que un
  símbolo no existía cuando estaba diez líneas más abajo. `file` lo llama `data`.

En código el uso legítimo es NUL como separador de clave compuesta
(`tenant‹NUL›user`): escríbelo **como escape**, nunca como byte de control. El
arreglo es byte-idéntico en runtime → ningún test se mueve.

Candado (el byte es invisible en el editor; no lo marcan linter ni typecheck):
un test que recorra `git ls-files` y falle si un fuente trae `0x00`.
⚠️ **Escribe el detector en un lenguaje que sepa expresar el byte**: en zsh,
`grep -qU $'\x00'` compila a **cadena vacía** → marca TODOS los ficheros. Uno que
dice «todo» falla igual de silenciosamente que uno que dice «nada» → fixture
negativo obligatorio. Detección puntual: `python3 -c "print(open('f','rb').read().count(b'\x00'))"`.
