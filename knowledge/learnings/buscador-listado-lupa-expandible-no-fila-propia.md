---
title: buscador de listado como lupa expandible, no fila propia ni inline fijo
date: 2026-07-14
source: claude-code-session
tags: [ui, frontend, ux]
---
Un input de búsqueda es elástico; si comparte fila de toolbar con controles de ancho fijo (pestañas de estado, orden, filtros), al crecer los estruja o fuerza wrap a 2 líneas. Y ponerlo en su propia fila deja un hueco vacío.

Patrón que funciona (Ley de Jakob, igual que el buscador del topbar): **lupa expandible** — en reposo es solo un icono en la barra de acciones (ocupa lo mínimo, cero hueco); al pulsar se expande a un input inline en la MISMA fila (width 0→N + opacity); al vaciar + blur / Escape se repliega. Componente reutilizable, no duplicar por listado.

Corolario de layout: en la toolbar, tabs a la izquierda con `flex:1 min-width:0 overflow-x:auto` (scrollan si no caben) + acciones `flex-shrink:0` a la derecha → todo en una línea sin que nada estruje a nada. Móvil: stack en columna aparte.
