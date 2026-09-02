---
title: Capturas guiadas para un cliente — marcar en el propio navegador con un overlay SVG, sin herramientas de imagen
date: 2026-09-02
source: facturaia
tags: [agent-browser, soporte, capturas, guia-cliente, qa]
---

Una guía paso a paso en un ticket necesita capturas con «pulsa aquí»: recuadro rojo, el resto oscurecido, etiqueta con el número de paso. En esta Mac no hay PIL ni ImageMagick, y no hacen falta: se inyecta un `<svg>` fijo sobre la página **antes** del `screenshot`.

- Helper: `~/.claude/bin/browser-spot.js` → `agent-browser --session X eval "$(cat ~/.claude/bin/browser-spot.js)"` y luego `eval "__spot([{el: '.selector' | elemento | {getBoundingClientRect}, label: '1. Pulsa…', pos: 'above'|'below'|'right'}])"`. Un `path` con `fill-rule: evenodd` hace el velo con N agujeros; `__byText(sel, regex)` localiza por texto (insensible a mayúsculas: el CSS `uppercase` engaña al `textContent`).
- El helper también oculta la franja `Modo vista` de la impersonación, el `billing-banner` y el PWA prompt: sin eso el cliente ve «Salir» y «3 respuestas sin leer» que no son suyos.
- Gotchas: `[class*=banner]` casa con wrappers de página entera y deja la captura en blanco (usar clases exactas); el viewport por defecto son 633 px de alto y los botones de pie quedan fuera → `agent-browser set viewport 1280 860`; una etiqueta `right` sobre un botón lo tapa, mejor `above`.
- Verificar la captura con `Read` antes de subirla (dos veces salieron banners y etiquetas solapadas). Y en modo impersonación no hay escritura: para enseñar casillas activas y el 409 de aprobar hay que ser miembro real (membresía temporal en org `is_test`, y borrarla).

Relacionado: [[agent-browser-verificar-snapshot-no-solo-screenshot]] · [[agent-browser-screenshot-cuelga-apps-con-polling]]
