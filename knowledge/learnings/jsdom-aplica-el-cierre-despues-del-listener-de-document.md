---
title: en jsdom el estado se aplica después del listener de document, en el navegador antes
date: 2026-09-13
source: facturaia
tags: [testing, react, jsdom, playwright]
---
Un menú dentro de un panel: el menú maneja Escape, hace `preventDefault` y se cierra;
el panel escucha Escape en `document` y se cierra si no hay menú abierto.

- **Navegador**: React aplica el `setState` del handler ANTES de que el evento llegue a
  `document`. La ref del menú abierto ya vale `null`, así que el mismo Escape cierra los dos.
  El guard correcto es `if (e.defaultPrevented) return` en el listener de `document`.
- **jsdom**: con `fireEvent` dentro de `act()`, el estado se aplica DESPUÉS. La ref todavía
  tiene el menú, el guard no hace falta y el test pasa igual con y sin él.

Consecuencia: **quitar el guard es un mutante que sobrevive en jsdom**. Un test unitario no
puede demostrar que ese guard hace falta; hace falta un smoke en el motor real. Vale para
cualquier pareja handler-de-componente ↔ listener global (Escape, click fuera, atajos).

**Confirmado en producción el 13-sep** conduciendo `app.tufacturaia.com`: con el menú de una
notificación abierto, el primer Esc cierra solo el menú y el segundo el panel. El smoke cuesta
cinco minutos y es la única prueba que existe de ese guard.
Ver [[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]] · [[un-bloque-de-comentario-sin-cerrar-se-come-el-resto-del-fichero]]
