---
title: css modules composes glass-panel/scrim from global
date: 2026-06-30
source: claude-code-session
tags: [css, frontend, glass, facturaia]
---

Aplicar tokens glass (`.glass-panel`, `.glass-sheen`, `.scrim`) a un CSS Module:

```css
.panel {
  composes: glass-panel glass-sheen from global;
  /* NO poner background: aquí — la clase global lo provee */
  border-radius: 14px;
  position: relative; /* necesario si hay hijos absolute */
}

.overlay {
  composes: scrim from global;
  position: fixed;
  inset: 0;
  /* NO poner background: aquí */
}
```

- `composes` añade los nombres de clase globales al elemento; las propiedades locales que repitan la misma prop que la global **ganan en orden de fuente** → eliminarlas del módulo
- `backdrop-filter` en `glass-panel`/`scrim` crea stacking context → z-indices de hijos son locales a esa superficie
- Usar en cualquier modal/drawer/panel nuevo para consistencia visual con el resto de la app
