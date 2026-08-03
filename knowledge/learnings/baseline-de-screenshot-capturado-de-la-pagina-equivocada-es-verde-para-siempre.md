---
title: un baseline de screenshot capturado de la página equivocada queda verde para siempre
date: 2026-08-03
source: claude-code-session
tags: [playwright, testing, gate, gotcha, facturaia]
---

`--update-snapshots` guarda lo que haya en pantalla, sea lo que sea. Si la ruta
redirige (auth, flag de entorno, 307), el spec fotografía la página de destino y
la comiteas como referencia. A partir de ahí el gate compara **login contra
login**: pasa siempre y no vigila nada. No se descubre nunca, porque el trabajo
de un baseline es precisamente pasar.

Caso FacturaIA (03-ago): `/design-system` solo es pública fuera de producción;
contra un servidor que no cumplía la condición devolvía 307 a `/login`. El
baseline `-darwin` comiteado ERA la pantalla de login. El `-linux` (generado en
el container) sí era la galería, así que el fallo solo afectaba a las tandas
locales — donde de verdad se corre.

Regla: **todo spec visual asierta dónde ha aterrizado antes de capturar** (URL +
un elemento propio de esa página). Y ocultar los adornos del entorno de
desarrollo (`nextjs-portal`, indicadores de compilación) que aparecen o no según
el momento, o el gate se vuelve una moneda al aire y se aprende a ignorarlo.
Relacionado: [[e2e-baseline-contra-main-antes-de-culpar-a-tu-rama]].
