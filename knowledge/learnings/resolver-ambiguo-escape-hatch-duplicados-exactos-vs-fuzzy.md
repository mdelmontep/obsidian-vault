---
title: un escape-hatch que colapsa ambigüedad a "el más reciente" solo vale para duplicados EXACTOS
date: 2026-07-08
source: claude-code-session
tags: [resolver, entity-matching, fuzzy-match]
---
Patrón: un resolver de nombre→entidad empieza con match EXACTO; cuando hay varios candidatos
exactos (datos sucios duplicados), un escape-hatch razonable es coger el más reciente en vez de
preguntar "¿cuál?" (no hay forma de distinguirlos, son literalmente el mismo string).

Gotcha: si luego añades capas de match PARCIAL o DIFUSO (fuzzy/Levenshtein) al mismo resolver
para resolver referencias por voz, ese escape-hatch se dispara TAMBIÉN para candidatos que
ahora SÍ se pueden distinguir por nombre (p. ej. "Marta López" vs "Marta Sánchez" al buscar
"Marta") — y enlaza a ciegas la cuenta equivocada en vez de preguntar.

Fix: el resultado "ambiguous" del resolver necesita un discriminador (p. ej.
`exactDuplicate: boolean`) que diga de qué CAPA vino la ambigüedad. El escape-hatch de
colapsar-al-más-reciente solo aplica cuando `exactDuplicate=true`; toda ambigüedad de
capas más laxas (parcial/fuzzy) debe preguntar siempre, nunca adivinar.
