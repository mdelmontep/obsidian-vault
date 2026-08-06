---
title: un guard de concurrencia que vivía de un side-effect deja de serializar cuando ese efecto se mueve a un trigger
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, concurrencia, refactor, triggers]
---

`UPDATE … WHERE estado IN (marcables)` serializa dos peticiones simultáneas **solo si
ese mismo UPDATE cambia `estado`**: el segundo llega y ya no casa. Si un refactor mueve
esa escritura a un trigger posterior, el guard sigue ahí, sigue leyéndose igual de
seguro y ya no protege — la ventana entre el UPDATE y el evento que dispara el trigger
deja pasar a los dos.

Caso TuFacturaIA (mig 640): al pasar `facturas.estado` a derivarse del ledger, marcar
cobrada dejó de escribirlo. Doble clic → dos filas de pago → `cobrado_eur` 2.662 sobre
un objetivo de 1.331. Reproducido en prod.

- Al convertir una columna en derivada, **grep de los guards que la usan como
  discriminante**. Un `WHERE col IN (...)` sobre una columna que ya no escribes ahí es
  un guard muerto que parece vivo.
- Fix mínimo sin RPC nueva: bloqueo optimista sobre `updated_at` (`.eq('updated_at',
  leido)`), que el propio UPDATE mueve vía `set_updated_at`. El segundo afecta 0 filas.
- El test que lo fija no mira el resultado, mira que el UPDATE **cotejó** el token: el
  resultado es idéntico en el camino feliz, y por eso el bug sobrevivió a la suite.

Pariente de [[atribucion-quien-usa-x-ahora-columna-escalar-pierde-bajo-concurrencia]] ·
[[columna-derivada-por-recompute-solo-admite-un-escritor]]
