---
title: modal sin portal montado en sidebar sticky queda bajo el contenido de main
date: 2026-06-09
source: claude-code-session
tags: [frontend, css, modal, stacking-context, z-index, nextjs, react]
---

Un `Modal` con backdrop `position:fixed; z-index:1000` que **no usa `createPortal`** se renderiza inline donde se invoca. Si un ancestro crea **stacking context**, el z-index queda atrapado en ese subárbol y puede perder contra contenido z:auto de otro subárbol.

Caso real TuFacturaIA (feedback widget): el modal colgaba del `<aside class="sidebar">` que es `position:sticky` (sticky **crea stacking context**, igual que transform/filter/opacity<1/will-change/isolation). El backdrop z:1000 quedaba scoped dentro del sidebar; como `<aside>` va antes que `<main>` en el DOM y ambos son z:auto a nivel `app-shell`, **`<main>` se pintaba encima** → en el dashboard los KPI cards tapaban los botones del modal (no clicables). Los otros 48 modales se montan dentro de `<main>`, por eso nunca lo sufrieron.

## Diagnóstico

`document.elementsFromPoint(cx,cy)` con el modal abierto: el primer elemento era el KPI card (z:auto), el backdrop salía el último. Recorrer ancestros del backdrop buscando lo que crea stacking context (NO solo transform — también `position:sticky/fixed`, `opacity<1`, `isolation`, `will-change`, `contain`) clavó el `sticky` del sidebar.

## Fix

`Modal` renderiza vía `createPortal(jsx, document.body)` → sale al stacking root, z-index global. Guard `mounted` (useState→useEffect) para no llamar createPortal en SSR. Antes de portar un componente compartido: grepear que ningún consumidor tenga `<form>` **envolviendo** al `<Modal>` (submit nativo no cruza el portal; si el form está *dentro*, portan juntos y funciona). Commit `c3998c5`. Relacionado: [[popover-en-modal-con-overflow-hidden-se-corta-usar-inline-disclosure]].
