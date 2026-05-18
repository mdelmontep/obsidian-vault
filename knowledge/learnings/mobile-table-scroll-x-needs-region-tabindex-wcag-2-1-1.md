---
title: mobile — tablas con scroll-x necesitan role=region + tabIndex + aria-label
date: 2026-05-18
source: facturaia FASE 2 mobile polish
tags: [frontend, a11y, wcag, tabla, mobile]
---

Envolver una `<table>` ancha en `<div style={{overflowX:'auto'}}>` para móvil **falla WCAG 2.1.1 (Keyboard)** si el wrapper no es focusable: el usuario de teclado no puede hacer scroll horizontal porque no hay manera de focusear el contenedor scrolleable.

**Patrón correcto**:

```jsx
<div role="region" tabIndex={0} aria-label="Tabla de usuarios" className="set-table-wrap">
  <table style={{ minWidth: 600 }}>...</table>
</div>
```

```css
.set-table-wrap {
  overflow-x: auto;
  border-radius: inherit;
}
.set-table-wrap:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}
```

- `role="region"` + `aria-label` único por tabla anuncia la región al SR.
- `tabIndex={0}` hace el div focusable para que el usuario pueda Tab → flechas para scroll.
- El `<table>` mantiene su role implícito intacto al envolverlo en el div.
- Una clase reusable evita el patrón de inline-style duplicado ×N. Caso FacturaIA: ×5 en settings + api-keys.

`WebkitOverflowScrolling: 'touch'` es legacy (iOS 13+ default) — no añadir.
