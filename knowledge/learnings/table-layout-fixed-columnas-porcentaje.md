---
title: table-layout fixed: porcentajes deben sumar 100% o hay gaps
date: 2026-04-27
source: claude-code-session
tags: [css, tablas, frontend]
---

Con `table-layout: fixed`, si los anchos en % no suman 100%, el navegador distribuye el sobrante en columnas porcentuales creando gaps inesperados.

Ejemplo: cols al 13+19+10+10+9+10+9+10 = 90% → 10% extra repartido, una col se infla y los elementos quedan desalineados.

**Fix**: definir clase variante en la tabla (`has-vf`, `has-origen`) y sobreescribir anchos para esa variante sumando exactamente 100%.

Si hay columnas de px fijas (36px, 40px), descontarlas del 100% mental antes de repartir porcentajes.
