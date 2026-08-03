---
title: dos modales que se cierran a la vez dejan el body sin scroll para siempre
date: 2026-08-03
source: claude-code-session
tags: [frontend, react, css, modales, accesibilidad]
---

Patrón: cada `Modal` guarda el `document.body.style.overflow` que había al abrirse y lo
restaura en su cleanup. Cerrando de uno en uno (LIFO) funciona. Pero si dos se desmontan
en el **mismo commit de React** (un `setNiveles([])` que cierra una pila entera), los
cleanups corren de fuera hacia dentro: el de fuera restaura `''` y el de dentro escribe
`'hidden'` **después**. La página queda sin scroll, sin error en consola y sin nada roto
en el DOM. Fallo silencioso puro.

El foco tiene el mismo problema en menor grado: cada nivel restaura el elemento que lo
tenía al abrir, y con cierre simultáneo el último apunta a un nodo que se desmonta.

Fix: para navegación apilada, **un solo `Modal` con la pila como estado interno**, nunca
un modal por nivel. Si el modal expone un ref a su cuerpo, sirve para devolver el scroll
arriba al cambiar de nivel.

No lo resuelve la pila de Escape: eso arregla el teclado, no el scroll-lock. Ver
[[escape-en-overlays-una-sola-pila-lifo]].
