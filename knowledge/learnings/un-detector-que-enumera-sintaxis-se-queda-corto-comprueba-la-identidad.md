---
title: un detector que enumera sintaxis se queda corto; comprueba la identidad
date: 2026-08-03
source: claude-code-session
tags: [gates, eslint, guards, auditoria, metodo]
---

Es S19 —«los privilegios se conceden por enumeración y **no se quitan** por enumeración»—
aplicado a un detector: enumerar FORMAS de escribir algo es una lista que siempre se queda
corta, y cada agujero se descubre de uno en uno.

Casos, todos por auditoría adversarial, nunca por revisión normal: G-SSRF (alias de `fetch`,
arreglo real `no-restricted-globals` por REFERENCIA) · gate de acciones (`export const` dejaba
pasar `export { X }`/`default`/`let`/`var`/`function*`) · 4-ago: G-D11 (tabla entrecomillada),
G-S4 (secreto por corchetes), G-TOKENS (substring sin límite de palabra).

**Variante hallada el 5-ago, misma familia con otra cara**: comprobar la PRESENCIA de un import
del módulo correcto en el fichero no es comprobar que ESE VALOR concreto venga de ahí — un
import señuelo sin relación con el relleno lo satisfacía (G-S5: `plan` de `V1Deps`; G-ROUTE-
WRAPPER y G-ADMIN-ACCION: un comentario citando el import bastaba, sin quitar comentarios antes
de buscar; G-ACCESS-DRIFT: una política manual más reciente que el "ganador" no entraba en la
comparación). Arreglo real: trazar identificador→asignación→llamada→import, no solo "¿existe el
import en algún sitio del fichero?".

**Señal de parar: la tercera variante de la misma regla.** Ahí toca identidad (símbolo resuelto,
import trazado), no un caso más.

Ver [[un-guard-enumera-la-clase-que-la-regla-escrita-solo-documenta]] ·
[[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]
