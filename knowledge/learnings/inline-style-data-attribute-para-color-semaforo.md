---
title: data-attribute para color runtime en semáforos evita inline style
date: 2026-06-15
source: claude-code-session
tags: [css, react, frontend]
---

Proyectos con trinquete de inline-styles bloquean `style={{ color: valor_runtime }}`.

Patrón: usar `data-*` + CSS attribute selector.

```tsx
<span className="semaforo" data-estado={salud.semaforo}>●</span>
```

```css
.semaforo { color: var(--muted); }
.semaforo[data-estado="verde"]   { color: var(--ok-fg); }
.semaforo[data-estado="naranja"] { color: var(--warning-fg); }
.semaforo[data-estado="rojo"]    { color: var(--danger-fg); }
```

Funciona con CSS Modules, globals y Tailwind (via `data-[estado=verde]:text-green-*`).
Elimina el `style={{}}` sin perder dinamismo; el valor viene del JS, el estilo del CSS.
