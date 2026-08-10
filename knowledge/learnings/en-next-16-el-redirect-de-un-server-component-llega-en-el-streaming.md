---
title: en next 16 el redirect de un server component llega en el streaming, no en la respuesta
date: 2026-08-10
source: claude-code-session
tags: [nextjs, e2e, testing, gotcha]
---
FacturaIA 10-ago: `/fiscal/2026/303/2T` "respondía 200 y no montaba su contenido". Falso: el
`page.tsx` hace `redirect('/')` (módulo en `proximamente`) y **ese redirect llega en el streaming**.

Medido con el navegador: a los **0 s** la URL sigue siendo la pedida y el status es **200**; a los
**4 s** está en `/` con el `h1` del dashboard. Un diagnóstico previo lo leyó como «responde 200 y la
URL se mantiene» — era verdad y era una redirección diferida, así que se buscó la causa donde no
estaba (add-on de la org) en vez de en el interruptor global del módulo.

Lo mismo con `notFound()`: la cáscara se sirve con **200** y el 404 llega después, así que
`expect(resp.status()).toBe(404)` falla con la guarda perfectamente puesta.

**Regla**: bajo renderizado parcial, afirmar sobre **lo que se pinta**, nunca sobre `status()` ni
sobre el primer instante. `page.waitForURL(...)` y aserciones web-first (`toHaveCount`,
`toBeVisible`), que reintentan, en vez de `waitForTimeout` + lectura única.
