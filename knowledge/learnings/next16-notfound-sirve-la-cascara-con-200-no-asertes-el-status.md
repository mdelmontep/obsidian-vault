---
title: con renderizado parcial, notFound() sirve la cáscara con 200 — no asertes el status
date: 2026-08-10
source: claude-code-session
tags: [nextjs, next16, testing, playwright, e2e]
---
Next 16 con Cache Components: una página parcialmente prerenderizada (`◐` en la salida del
build) sirve su **cáscara estática con HTTP 200** y el contenido dinámico llega por
streaming. Si el `notFound()` está en la parte dinámica, `response.status()` sigue siendo
**200** aunque el usuario vea la pantalla de "no existe".

FacturaIA 10-ago: un smoke asertaba `expect(resp.status()).toBe(404)` para una combinación
imposible de modelo+periodo. Falló con 200 y parecía un fallo de la guarda del `page.tsx`.
La guarda estaba bien; el test asertaba lo que ya no se puede asertar.

**Fix**: asertar lo que se PINTA (el heading de la página de error), no el código HTTP.
Sirve además para el caso general: bajo streaming, el status de la respuesta ya no resume
el resultado del render.

Cuidado con la lectura inversa: un `curl` sin sesión a esa misma ruta devuelve **307** (el
proxy manda a `/login`), así que tampoco vale como comprobación del 404.

Ver [[next16-cache-components-migracion-por-etapas]].
