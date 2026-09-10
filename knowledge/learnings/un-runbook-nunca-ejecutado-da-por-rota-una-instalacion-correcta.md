---
title: un runbook nunca ejecutado da por rota una instalación correcta
date: 2026-09-10
source: mandadm
tags: [documentacion, metodo, verificacion, runbook]
---
`docs/deploy/supabase.md` estaba escrito con cuidado y citando docs oficiales, y **nadie lo había
corrido nunca**. Al ejecutarlo contra el primer despliegue real, **tres** de sus comprobaciones eran
falsas:

- «`anon` y `authenticated` deben dar `false` sobre `ops`» — `authenticated` lo tiene a `true` a
  propósito, y el propio test del repo lo **exige**.
- «`select … from ops.events` debe fallar con permission denied» — devuelve **cero filas** por RLS.
- «las siete tablas», enumerando ocho.

Las tres van en la misma dirección: seguirlo al pie de la letra habría hecho **dar por rota una base
recién desplegada y correcta**, y el arreglo habría sido romperla de verdad.

Un runbook derivado de documentación es una **hipótesis**, no una comprobación, por muy bien escrito
que esté. La primera ejecución real no es «seguir los pasos»: es **auditar cada aserto contra el
sistema** y corregir el fichero en el mismo commit.
Ver [[un-200-no-prueba-que-la-pagina-citada-exista]] · [[la-suposicion-de-un-agente-escrita-en-indicativo-se-lee-como-decision]]
