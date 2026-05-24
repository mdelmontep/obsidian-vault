---
title: react inputs numéricos — state string > state number (cursor + 0 editable)
date: 2026-05-24
source: claude-code-session
tags: [react, forms, controlled-inputs, ux]
---

`<input type="number" value={0} onChange={e => set(Number(e.target.value))}>` con state `number` tiene 2 problemas UX:
- El `0` inicial deja el cursor anclado tras él → user tiene que escribir `0850` y borrar el `0`. Imposible "seleccionar todo".
- Al borrar hasta vacío, React vuelve a renderizar `0` y el cursor salta.

**Patrón pro (Holded/Stripe)**: state `string`, parser lazy.
```ts
const [p, setP] = useState<string>('')   // no number
// onChange={e => setP(e.target.value)}
// onFocus={e => e.currentTarget.select()}  // select all
// placeholder="0,00"
// step="any"  // flecha sube 1, decimales aceptados sin :invalid
const valor = parseNumeroEs(p)            // parser robusto (ver [[parser-numero-es-bug-con-input-html5-number-punto-como-decimal-no-millares]])
```

`step="any"` evita que el browser flagee `12,50` como inválido vs `step={1}`. Aplica a cualquier campo monetario/cantidad de form React. Caso real FacturaIA sprint formulario facturas 2026-05-24 — bugs 3+4 cerrados con este patrón.