---
title: react-hooks/refs (React Compiler) marca refs.setFloating de floating-ui como falso positivo
date: 2026-06-18
source: claude-code-session
tags: [frontend, react, react-compiler, eslint, floating-ui]
---

Con React 19 + React Compiler, el lint `react-hooks/refs` marca `ref={refs.setFloating}`
/ `ref={refs.setReference}` de `@floating-ui/react` como "Cannot access ref during render".
Es un FALSO POSITIVO conocido: la heurística infiere que cualquier variable llamada `refs`
es un ref y trata acceder a sus props como leer `.current` en render (refs.setX no es eso).

Fix sin `eslint-disable`: que el hook propio exponga `setReference`/`setFloating` como
funciones TOP-LEVEL (no bajo un objeto `refs`). El consumidor hace `ref={setFloating}` →
nombre no-ref → no salta. Para leer el nodo en handlers, expón `getFloatingEl()`; para
foco, `focusReference()`. Menús con teclado: usar `<FloatingFocusManager>`.

Bonus: NO uses `useCallback` manual (dispara `react-hooks/preserve-manual-memoization`);
deja memoizar al compiler. Refs: floating-ui#3405, react#34775. Caso FacturaIA PR #376
(hook `useAnchoredMenu`). Ver [[menu-portal-flip-viewport]] · [[css-animation-transform-pisa-transform-estatico]].
