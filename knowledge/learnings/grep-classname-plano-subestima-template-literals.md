---
title: al auditar "0 consumidores" de una clase CSS, grep className="X" plano subestima — falta el patrón interpolado
date: 2026-07-16
source: claude-code-session
tags: [css, refactor, grep, react]
---
Al migrar/eliminar un dialecto CSS (ej. `.btn-*` global → primitivo React),
el grep típico `className="btn-*"` (string literal) solo captura la forma
plana. En React es habitual `` className={`btn-* ${extra}`} `` o
`className={cond ? 'btn-x' : 'btn-y'}` — ninguno matchea ese regex.

Caso real: conteo inicial "6 `<a>` + 21 `<Link>`" con `btn-*` (grep plano)
resultó ser ~30 ficheros más grande tras un barrido con
`grep -nE '\bbtn-[a-z]+\b'` (word-boundary, sin anclar a `className="`).

Fix: para dar un dialecto por "0 consumidores" y borrar su CSS, grepear con
regex de palabra completa (`\bclase-x\b`) sobre TODO el string del archivo,
no solo dentro de `className="..."` literal — cubre template literals,
ternarios y concatenaciones. Repetir el grep tras cada tanda de migración
antes de declarar el frente cerrado.
