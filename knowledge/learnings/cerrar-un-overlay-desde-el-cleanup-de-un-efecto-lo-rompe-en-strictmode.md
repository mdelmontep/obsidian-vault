---
title: cerrar un overlay desde el cleanup de un efecto lo rompe en StrictMode
date: 2026-07-25
source: claude-code-session
tags: [react, nextjs, modales, strictmode, facturaia]
---

Patrón tentador con Cache Components / `<Activity>` de Next 16: como al ocultar una ruta React limpia sus efectos, se usa el cleanup para cerrar un overlay portaleado a `body`.

```js
useLayoutEffect(() => () => close(), [])   // ← roto
```

En desarrollo React monta, desmonta y remonta cada efecto a propósito, justo para detectar este acoplamiento. Ese desmontaje sintético dispara el cierre **en el mismo instante en que el overlay se abre**.

Síntoma engañoso: "el modal no abre". Sin error en consola, sin nada en el DOM, y con el foco de vuelta en el botón que lo lanzó, que es exactamente lo que hace el propio modal al cerrarse. Fácil de atribuir al último cambio funcional en vez de al primitivo.

Fix: aplazar la decisión un microtask, de modo que un remontaje la cancele.

```js
useLayoutEffect(() => {
  montado.current = true
  return () => { montado.current = false
    queueMicrotask(() => { if (!montado.current) close() }) }
}, [])
```

Regla general: **el cleanup de un efecto no distingue "me estoy yendo" de "me están remontando".** Si la acción no es idempotente (cerrar, cancelar, notificar, liberar un lock), no la dispares síncronamente ahí.

Caso real: FacturaIA, `d35b70a5` (#1140), cuyo propio título decía "[WIP · no mergear sin QA]". Rompía TODOS los modales en local. Ver [[facturaia-modulo-sepa-config]].
