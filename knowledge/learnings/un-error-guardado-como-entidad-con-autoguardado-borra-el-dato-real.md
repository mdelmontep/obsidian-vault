---
title: un error guardado como entidad, con autoguardado al desenfocar, borra el dato real
date: 2026-09-13
source: facturaia
tags: [react, fetch, rate-limit, autosave, integridad]
---

`fetch(url).then(r => r.json()).then(setEntidad)` no mira `res.ok`: un 429 (o 403, 500) mete
`{ error: 'rate_limited' }` en el estado como si fuera la entidad. El formulario se pinta con los
campos vacíos y **editables**, y si guarda al desenfocar, salir del campo manda `nif: ''` sobre la
fila real. El fallo de red se convierte en escritura destructiva sin que nadie teclee nada.

Patrón: lectura por un helper que lanza en no-2xx (`fetchJson`), estado de error explícito con
reintento en vez del formulario, y una recarga que falla conserva lo que ya había. Mismo defecto,
otras caras: una lista que recibe un objeto revienta la página entera al hacer `.map`, y un `if
(res.ok)` sin `else` pinta «Sin resultados», que es una afirmación falsa, no un fallo.

Barrido: `grep -rn "res.json()" | grep -v "res.ok"` en vistas con autoguardado primero.
Caso real: ficha de org en /admin de TuFacturaIA, límite 120/min (#2752, PR #2758).
