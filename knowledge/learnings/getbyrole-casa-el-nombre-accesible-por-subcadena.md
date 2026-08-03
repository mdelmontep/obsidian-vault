---
title: getByRole casa el nombre accesible por subcadena, y .first() elige por ti
date: 2026-08-03
source: claude-code-session
tags: [playwright, e2e, testing, a11y, facturaia]
---

`page.getByRole('button', { name: 'X' })` **no** exige nombre exacto: busca
subcadena, sin distinguir mayúsculas. Si otro control se llama `X <algo>`, entra
en el mismo locator, y `.first()` se queda con el que va antes **en el DOM**, no
con el que quieres.

Caso real (smoke de obras, roto 30 días sin que nadie lo viera): dos botones,
`Añadir partida al capítulo <nombre>` en la cabecera del capítulo —que solo
mueve el foco a la fila de alta— y `Añadir partida al capítulo` a secas, el que
envía. `.first()` cogía el de la cabecera.

**Lo peligroso es cómo falla.** El botón equivocado existe, es visible y se deja
pulsar, así que el click NO da error: simplemente no ocurre nada, y el test
muere después en el `waitForResponse` con toda la pinta de un bug de la
aplicación. Se persiguen el endpoint y la migración antes de mirar el locator.

**Fix:** `{ name: '…', exact: true }` y quitar el `.first()`. Y al añadir un
`aria-label` que sea prefijo de otro, asume que acabas de fusionar dos locators.

Ver [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
