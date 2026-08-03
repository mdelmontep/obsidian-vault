---
title: un detector que enumera sintaxis se queda corto; comprueba la identidad
date: 2026-08-03
source: claude-code-session
tags: [gates, eslint, guards, auditoria, metodo]
---

Es S19 —«los privilegios se conceden por enumeración y **no se quitan** por enumeración»—
aplicado a un detector: enumerar FORMAS de escribir algo es una lista que siempre se queda
corta, y cada agujero se descubre de uno en uno.

Dos casos el mismo día, los dos encontrados por una auditoría adversarial:

- **G-SSRF** vigilaba `fetch(...)` y `globalThis.fetch`. Se rodeaba con `const traer = fetch`
  (verificado: `eslint` daba **cero** errores). Al cerrar el alias aparecieron `function f(x =
  fetch)` y `export { fetch }`. La salida no era el selector número quince: fue
  `no-restricted-globals`, que marca cualquier **referencia** al global mire donde mire.
- **Un gate de acciones de servidor** buscaba `export const`. Se le escapaban `export { X }`,
  `export default`, `export let`, `var` y `function*` — y Next expone las cinco igual como
  endpoints invocables.

**La señal de parar: cuando estás añadiendo la tercera variante de la misma regla.** Ahí ya no
toca un caso más, toca una comprobación que no dependa de la forma (el símbolo resuelto, el
import, la procedencia). Los selectores por sintaxis se quedan solo para lo que la
comprobación por identidad no ve.

Ver [[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]] ·
[[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]
