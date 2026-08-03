---
title: un token definido bajo un selector que nadie produce no existe en ejecución
date: 2026-08-03
source: claude-code-session tucrmia
tags: [css, tokens, gates, fallo-silencioso, nextjs]
---

Los tokens de tema suelen vivir en `:root[data-theme="light|dark"]`. Si la app **nunca escribe
ese atributo**, ninguna de esas reglas casa: los 86 tokens de color, radio, sombra y
`--focus-ring` están escritos, pasan cualquier comprobación de «está definido», y **no existen**.
El navegador se queda con lo heredado y sigue. Caso real: `layout.tsx` pintaba `<html lang="es">`
desde el commit 1, con 22 gates y 973 tests en verde y el fichero de tokens copiado de otro
producto donde sí se escribía.

**Comprobarlo es una línea contra el servidor construido**, no leyendo el CSS:
`curl -s localhost:PORT/ | grep -o '<html[^>]*>'`.

**El gate**: si TODOS los bloques que definen un token condicionan por un atributo, ese atributo
tiene que escribirlo la app. Por **nombre** y no por valor —que `[data-theme="dark"]` sea
inalcanzable con el tema claro es correcto—, y el hueco deliberado (un skin que no se activa) se
declara con un marcador en la propia hoja. Ojo: quita los comentarios del TS/TSX antes de buscar
el atributo, o el comentario que explica la regla la satisface
([[un-trinquete-que-cuenta-por-regex-tambien-cuenta-los-comentarios]]).

Familia: [[un-var-de-css-que-no-existe-no-falla-se-queda-con-lo-heredado]] (nombre inexistente) y
[[style-inyectado-con-root-pierde-contra-root-data-theme]] (pierde la cascada). Aquí el nombre
está bien y la cascada también: lo que falta es el selector.
