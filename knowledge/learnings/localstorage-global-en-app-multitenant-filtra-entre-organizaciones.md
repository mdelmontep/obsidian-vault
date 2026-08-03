---
title: localStorage global en app multi-tenant filtra preferencias entre organizaciones
date: 2026-08-03
source: FacturaIA — Ajustes › Apariencia (color de marca, skin, densidad, tema de pills)
tags: [multitenant, frontend, ssr, nextjs, seguridad-visual]
---

Preferencia guardada **por organización** en la BD pero restaurada desde una clave **global de
`localStorage`** = el tenant nuevo se pinta con la configuración del anterior. Dispara con
cualquier switch de empresa que recargue el documento: al arrancar, el cliente lee la clave —que
no distingue de quién es— y la aplica.

Lo tapaba otro fallo: el color, además, no se restauraba en absoluto (se escribía y nadie lo
leía), así que el síntoma visible era «no se guarda» y el de fondo no se veía. **Encender una
restauración muerta es un cambio de comportamiento**: mira de quién es el dato antes.

Olor: una lista de `getItem('af-*')` en el arranque del shell junto a un `savePreference` que
escribe en una tabla por tenant. Si no coinciden en número, hay una que se pierde; si coinciden,
hay una que se filtra.

Arreglo: sembrarlo en servidor sobre un SELECT del tenant que ya se hiciera. Cierra cross-org,
navegador sin caché y parpadeo de la primera pintura. Variables CSS → `:root` en un `<style>`;
atributos `data-*` → script inline con los valores filtrados contra un `Record<Union, true>`.

Ver [[token-de-relleno-no-sirve-como-token-de-texto]].
