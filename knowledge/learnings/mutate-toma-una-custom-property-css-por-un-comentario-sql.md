---
title: mutate rechaza anclar en una custom property CSS por confundir `--` con un comentario
date: 2026-09-09
source: facturaia
tags: [mutate, css, arnes, falso-positivo, gotcha]
---
`~/.claude/bin/mutate` se niega a mutar una cadena que parezca comentario, y avisa de que mutar
un comentario no prueba nada. La heurística incluye el `--` inicial (comentario en SQL), así que
**toda custom property CSS lo dispara**: anclar en `  --radius-md: 8px;` sale rechazado aunque
sea una línea que se ejecuta.

No es un bug del arnés, es su detector siendo conservador con un lenguaje donde `--` significa
otra cosa. Y `--permitir-comentario` es la salida equivocada aquí: apagaría el detector en vez
de anclar bien.

Ancla en algo del mismo bloque que no empiece por `--`. El selector va perfecto y además muta
mejor, porque deja meter la declaración dentro del bloque equivocado, que es justo el bug que se
quiere reintroducir:

```
mutate src/app/tokens.css ':root[data-theme="light"] {' ':root[data-theme="light"] { --radius-md: 8px;' -- npx vitest run <test>
```
