---
title: un seed RSC con 'use cache' keyado por org ignora la impersonación y sirve datos de la org anterior
date: 2026-07-28
source: claude-code-session
tags: [nextjs, cache-components, multitenant, impersonation, supabase]
---

En modo vista de superadmin (cookie `impersonate_org`), el listado de facturas mostraba **las filas de la org anterior** mientras los contadores de las pestañas ya eran los de la org impersonada. Los datos solo se corregían al tocar un filtro, que es cuando entra el hook cliente y hace su propio fetch.

La causa: el seed de servidor va por un envoltorio `'use cache'` keyado por `orgId`, y ese `orgId` se resuelve **fuera** del scope cacheado, por `profiles.active_org_id` — no por la cookie de impersonación. Resultado: dos fuentes de verdad sobre "qué org estoy viendo" y una de ellas se salta la impersonación.

Cómo se nota: cabecera y cuerpo de la misma pantalla discrepan. Si solo miras los totales, parece que funciona.

Regla: **cualquier resolución de tenant que alimente una caché debe pasar por el MISMO helper que usa el request** (el que ya mira la cookie), nunca leer la columna del perfil por su cuenta. Y al probar impersonación, comparar filas contra contadores, no solo el rótulo de la cabecera.

Caso real 2026-07-28, TuFacturaIA (visto en vivo, no inferido). Pariente de [[cookie-impersonate-leak-fuera-de-admin]].
