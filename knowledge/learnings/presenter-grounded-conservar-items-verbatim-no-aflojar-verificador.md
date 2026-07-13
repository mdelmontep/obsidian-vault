---
title: presenter LLM grounded — conserva los ítems verbatim, no aflojes el verificador
date: 2026-07-13
source: claude-code-session
tags: [agentes, llm, grounding, prompt-engineering]
---
Al poner una capa LLM que "presenta" datos calculados en código (reads fraseados, listas bonitas) con
un verificador determinista de grounding, el check "todos los ítems presentes" hecho como SUBSTRING
CONTIGUO del ítem completo es demasiado estricto con ítems COMPUESTOS ("Perfiles Java (etapa: X) · 80.000 €"):
la reformulación en prosa parte el ítem → falso negativo → fallback constante aunque el LLM sea fiel.

Fix correcto: NO aflojar el verificador (debilita la garantía "el LLM solo reformula, no inventa").
En su lugar, RESTRINGIR EL PROMPT DEL PRESENTER a conservar cada ítem letra a letra y reformular solo
la introducción + encadenarlos en una frase. Así pasa el grounding estricto sin tocarlo. Medido con
smoke real (gpt-4o-mini): 2/5 → 5/5 grounded, fiel y natural. Es el prompt del presenter (barato,
aislado), no el del interpreter. Corolario: valida siempre con un smoke real que mida la TASA DE
FALLBACK — un guard demasiado estricto = fallback constante = el presenter no aporta nada.
Ver [[structured-outputs-strict-garantiza-forma-no-veracidad]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]].
