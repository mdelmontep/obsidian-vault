---
title: un detector que enumera sintaxis se queda corto; comprueba la identidad
date: 2026-08-03
source: claude-code-session
tags: [gates, eslint, guards, auditoria, metodo]
---

Es S19 —«los privilegios se conceden por enumeración y **no se quitan** por enumeración»—
aplicado a un detector: enumerar FORMAS de escribir algo es una lista que siempre se queda
corta, y cada agujero se descubre de uno en uno.

Casos, todos encontrados por auditoría adversarial, nunca por revisión normal:

- **G-SSRF**: `fetch` vigilado por nombre, rodeado con `const traer = fetch`; al cerrarlo,
  `function f(x = fetch)` y `export { fetch }` seguían colando. Arreglo real:
  `no-restricted-globals`, que marca la REFERENCIA, no la forma.
- **Gate de acciones de servidor**: buscaba `export const`; se le escapaban `export { X }`,
  `default`, `let`, `var`, `function*` — Next expone las cinco igual.
- **4-ago, tres más en una sola auditoría**: G-D11 no veía una tabla entrecomillada
  (`"profiles"`) en el SQL; G-S4 no veía un secreto accedido por corchetes
  (`fila['token_hash']`, el selector solo miraba `.name`, no `.value` de un `Literal`);
  G-TOKENS daba por escrito `data-theme` con solo `.includes()`, que un futuro
  `data-theme-preview` habría satisfecho sin límite de palabra.

**La señal de parar: cuando estás añadiendo la tercera variante de la misma regla.** Ahí toca
una comprobación que no dependa de la forma (símbolo resuelto, import, identidad), no un caso
más.

Ver [[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]] ·
[[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]
