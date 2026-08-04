---
title: exactOptionalPropertyTypes con una prop CSS-module da string|undefined, no solo string
date: 2026-08-04
source: tucrmia — Panel className/subtitle en pantalla.tsx
tags: [typescript, css-modules, nextjs, gotcha]
---

Con `exactOptionalPropertyTypes: true`, pasar `className={estilos.miClase}` a una prop tipada
`className?: string` falla en typecheck si el tipo generado del `.module.css` (o el ambiente de
CSS-modules del proyecto) declara sus propiedades como `string | undefined` en vez de `string` —
lo normal, porque técnicamente cualquier clave puede no existir en el objeto. `exactOptionalPropertyTypes`
distingue "prop ausente" de "prop presente con valor `undefined`", y `estilos.miClase` es formalmente lo
segundo.

**No sirve** envolver con spread condicional (`{...(x ? {className: estilos.x} : {})}`) ni tipar la
variable a mano — el tipo de origen sigue siendo `string | undefined`. **El fix real es coalescer en el
punto de uso**: `estilos.miClase ?? ''`. Para props que solo deben aparecer condicionalmente (ej. un
`subtitle` que a veces no debe pintarse), usar un valor siempre-string en vez de `undefined` explícito
(`archivado ? 'Archivado' : ''`), no intentar omitir la prop dinámicamente.
