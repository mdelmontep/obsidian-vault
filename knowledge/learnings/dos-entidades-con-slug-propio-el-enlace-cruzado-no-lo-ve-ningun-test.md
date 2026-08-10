---
title: dos entidades con slug propio: enlazar con el equivocado no lo ve ningún test
date: 2026-08-11
source: claude-code-session
tags: [testing, frontend, gates]
---
Un tema y su lección tenían cada uno su `slug`: el del tema escrito a mano en un JSON, el de la
lección derivado del título que acabó poniéndole el generador. La página enlazaba
`/leccion/{tema.slug}`.

Coincidían mientras no hubo lecciones creadas desde el temario. En cuanto las hubo, **todos** los
temas ya estudiados llevaban a un 404 — y el temario es justo donde uno pulsa.

No lo cogió nada: lint, typecheck, 171 tests y build en verde. Cada pieza estaba bien por separado;
lo que fallaba era la unión.

Dos consecuencias que valen para cualquier proyecto:
- Cuando dos entidades tienen slug propio, el tipo debe **llevar el ajeno consigo** (aquí,
  `construirRuta` genérico en `T extends Tema` para que el slug de la lección viaje con el tema y lo
  sepa el compilador) en vez de rebuscarlo fuera.
- Hace falta un gate que **atraviese el sitio como una persona**: recorrer los enlaces con sesión y
  fallar si algo da 404, diciendo desde qué página se llegaba.
  Ejemplo: `learn-agentesia/scripts/mirar-enlaces.mjs`.
