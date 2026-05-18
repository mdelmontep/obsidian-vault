---
title: mobile — inert + aria-hidden complementarios para iOS 15.0-15.4
date: 2026-05-18
source: facturaia FASE 2 mobile polish
tags: [frontend, a11y, ios, safari, drawer, modal]
---

`inert` HTML attribute (Safari 15.5+, Chrome 102+, Firefox 112+) bloquea Tab + interacción puntero + lectura SR en el subárbol. Pero **iOS 15.0-15.4 lo ignora silenciosamente** → VoiceOver navega al contenido oculto + teclado externo Bluetooth tabula al main.

Añadir `aria-hidden={open || undefined}` en paralelo cubre VoiceOver en esa franja (no cubre Tab por teclado externo, pero el caso es minoría):

```jsx
<main inert={open || undefined} aria-hidden={open || undefined}>
```

React 19 reenvía `inert` boolean como atributo DOM (PR #24730). React 18 lo ignora — verificar versión antes de confiar en `inert`.

Ver [[mobile-restore-focus-after-inert-needs-raf]] · [[mobile-vh-dvh-cascade-vs-min-atomic-safari-15]].
