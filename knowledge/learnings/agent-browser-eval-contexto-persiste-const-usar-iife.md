---
title: agent-browser eval reutiliza el contexto JS — `const` redeclarado lanza "already declared"
date: 2026-07-13
source: claude-code-session
tags: [agent-browser, testing, qa]
---
Llamadas sucesivas de `agent-browser eval` comparten el mismo contexto de ejecución. Un
`eval "const b = ...; b.foo"` funciona la 1ª vez y a la 2ª lanza
`SyntaxError: Identifier 'b' has already been declared`. En un bucle de polling
(`for i ...; do agent-browser eval "const bar=...; ..."; done`) TODAS las iteraciones tras
la 1ª fallan → el script rompe en silencio y mide/decide mal (me dio un tiempo de QA falso).

Fix: envolver el snippet en un IIFE, sin declarar globals:
`agent-browser eval "(()=>{ const bar=document.querySelector('.x'); return bar?.textContent; })()"`
o usar nombres únicos por iteración. Para esperar una condición sin polling manual, mejor
`agent-browser wait --fn "<expr booleana>"` (poll interno, un solo comando, menos overhead
y sin contaminar el cronometraje). Ver [[agent-browser-cdp-formularios-react-requestsubmit]].
