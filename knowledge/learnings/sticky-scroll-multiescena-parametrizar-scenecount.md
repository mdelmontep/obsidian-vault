---
title: sticky scroll multiescena con escenas distintas por device requiere parametrizar sceneCount
date: 2026-04-15
source: claude-code-session
tags: [motion, scroll, react, responsive]
---

En un sticky-scroll donde todas las escenas están pre-montadas (patrón opacity-toggle), insertar o quitar escenas según isMobile no es trivial. Hay que parametrizar el contador en toda la máquina: getSceneIdx(p, count), getSceneProgress(p, idx, count), section height (count * vh), resetFrom, jumpToScene y los labels "N/M". Además, durante un resize mid-scroll el activeIdx puede quedar fuera de rango al bajar el count → usar siempre safeIdx = Math.min(activeIdx, count - 1) para los reads (caption, color) y evitar crashes.
