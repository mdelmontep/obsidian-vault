---
title: una vista en «Cargando…» con su API en 200 puede estar sin hidratar
date: 2026-09-01
source: facturaia
tags: [react, nextjs, qa, navegador, hidratacion]
---

Síntoma: una página se queda en «Cargando…» para siempre. La petición aparece en red con **200**,
la consola limpia, y recargar no cambia nada. No es la API ni tu rama: la vista está servida pero
**sin hidratar**, y despierta con el primer evento de ratón **real**.

Cómo distinguirlo, en este orden:
- Si el `fetch` de la vista ya respondió 200 y la pantalla sigue en «Cargando…», es hidratación.
- Un `left_click` del `computer` la despierta. Un `.click()` sintético desde `javascript_tool` **no**
  (mundo aislado), y buscar `__reactFiber$` con `Object.keys(el)` desde ahí tampoco lo distingue.
- **Antes de culpar a tu PR**: abre una vista preexistente del mismo shell. Si hace lo mismo, no es
  tu regresión (1-sep, facturaia: igual en el panel nuevo, en el de OCR y en `/admin/documents`).

Lo que costó por no mirar esto primero: red, consola, borrar `.next` y reiniciar el dev server.
Ver [[playwright-domcontentloaded-no-espera-hidratacion-rsc]] · [[facturaia]]
