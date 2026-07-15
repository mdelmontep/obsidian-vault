---
title: migrar en masa a un primitivo sin cambiar píxeles = alinear su geometría al legacy primero
date: 2026-07-15
source: claude-code-session
tags: [design-system, refactor, css, migracion]
---
Consolidar cientos de call-sites de una clase global (`.btn-*`) al componente primitivo (`<Button>`) da miedo por el cambio visual. Técnica para hacerlo INVISIBLE y en masa:

1. **Alinear el primitivo al look ACTUAL** antes de migrar nada: mide con `getComputedStyle` un nativo vs el primitivo (h, border-radius, padding, font-size, line-height) y ajusta el primitivo hasta que coincidan al píxel. El culpable típico del descuadre de altura es `line-height` (normal ~1.3 vs `1`).
2. **className-merge desbloquea los "omitidos"**: si el primitivo hace spread de `className`, un `<button className="btn-x ${s.foo}">` migra a `<Button variant="x" className={s.foo}>` sin perder nada — la clase legacy sigue aplicando sobre el `<button>` renderizado.
3. **Enforcement incremental**: trinquete que congela el conteo de nativos (permite bajar, bloquea subir) + regla de lint a `error` SOLO en la carpeta ya limpia (beachhead) y `warning` en el resto.
4. Deja nativo lo que NO es el primitivo: `<a>/<Link>` (sin `as`), dialectos con prefijo (`adm-btn-*`), `<label>`, icon-only/toggles.

**Cuándo NO aplica**: solo sirve para primitivos DROP-IN (`<button>`→`<Button>`, mismos children). Un primitivo COMPUESTO (`<Input>` = `div.field>label>wrap>input`+error) reestructura el DOM por call-site → migrarlo es refactor por-formulario con QA por-pantalla, NO fleet mecánico. Detéctalo antes de lanzar agentes.

Caso real FacturaIA: 1053→577 botones nativos en una sesión con fleets de agentes. Ver [[css-background-white-hardcoded-rompe-dark-mode-silencioso]].
