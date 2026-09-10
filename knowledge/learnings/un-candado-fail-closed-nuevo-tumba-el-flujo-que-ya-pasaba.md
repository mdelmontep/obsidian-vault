---
title: un candado fail-closed nuevo tumba el flujo que ya pasaba si nadie lo resta antes
date: 2026-09-10
source: facturaia
tags: [postgres, triggers, migraciones, disenio]
---
Un guard nuevo en un trigger compartido no solo rechaza lo que quieres rechazar: **cambia
la aritmética de todo lo que ya pasaba por ahí**. Si el candado dice «lo cerrado no es
facturable», el camino feliz que reparte cantidades (`least(pendiente, lo_que_llega)`)
sigue proponiendo el total viejo, choca contra el candado nuevo y **la operación entera se
cae**, no la línea de más.

Regla: quien añade el candado resta su magnitud **también en el lado que reparte**, en la
misma migración. En facturaia van juntos el `IF` del trigger y el `least` de la RPC de
aprobación (`v_cerrada`), y la migración se autoverifica **ejecutando** la función, no solo
comprobando que el texto cambió.

Tercera reincidencia en el mismo trigger: AL013 (mig 768), AL015 (mig 856) y AL016 (mig
884). El tell es siempre el mismo: el guard se prueba con el caso que debe rechazar y
nadie prueba el caso que **ya funcionaba**. Ver [[el-arnes-se-mide-a-si-mismo]].
