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

**`glass-panel` (42-46% opaco) vs `glass-strong` (90% opaco)**: elegir por densidad de
contenido, no por defecto. `glass-panel` es para paneles decorativos sin datos densos
(drawer de chat IA). Un modal lleno de cifras/texto (facturas, importes) necesita
`glass-strong` — con `glass-panel` ahí el contraste cae y el texto se vuelve ilegible
contra el fondo difuminado (caso real: modal de conciliación manual, bajaba el contraste
por usar `glass-panel` en una lista de facturas con importes).

- **Modal CENTRADO con texto**: imitar el patrón canónico "doble cristal" de `src/components/ui/modal.module.css` (marco translúcido + placa interior `glass-bg-strong` ~90% que sostiene el texto). Caso 2026-07-02: submodales de conciliación se veían super-transparentes/ilegibles con `glass-panel` suelto → fix a `glass-bg-strong` + tratamiento del marco; verificado con test de contraste Playwright (13-17:1 AA).
