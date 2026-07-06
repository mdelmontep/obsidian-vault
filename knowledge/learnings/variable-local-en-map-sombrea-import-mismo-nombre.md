---
title: variable local dentro de un .map() puede sombrear un import con el mismo nombre
date: 2026-07-06
source: claude-code-session
tags: [frontend, react, javascript, gotcha]
---

Patrón: `import { Icon } from './icon'` a nivel de módulo, y dentro de un
`.map(it => { const Icon = it.icon; ... })` se reusa el mismo nombre `Icon`
para otra cosa (aquí, el icono propio del item). Todo el resto del closure del
callback queda sombreado — cualquier `<Icon name="x" />` posterior en ese mismo
bloque ya NO es el import, es la variable local, y renderiza silenciosamente
otra cosa (sin error de compilación ni de lint).

Caso real: `nav-section.tsx` — el candado de items de menú bloqueados por plan
renderizaba el icono del propio item duplicado en vez de un candado, porque
`<Icon name="lock" />` dentro del `.map()` llamaba a `it.icon` (un componente
lucide que ignora `name`), no al wrapper importado.

Fix: nombrar la variable local de forma distinta al import (`ItemIcon`, no
`Icon`). Al revisar código con imports de un solo nombre corto/genérico
(`Icon`, `Item`, `Field`…), grep del nombre dentro de callbacks anidados antes
de dar por bueno el render.
