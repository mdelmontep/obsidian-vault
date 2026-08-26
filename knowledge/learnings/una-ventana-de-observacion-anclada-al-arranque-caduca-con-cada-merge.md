---
title: una ventana de observación anclada al arranque caduca con cada merge
date: 2026-08-26
source: agh-iberica
tags: [deploy, verificacion, metodo, observabilidad]
---
Para verificar «¿emite el emisor ya encendido?» di una ventana: *mira filas posteriores a las 19:05*.
La corregí a 19:55 y volvió a caducar sola. **Tres arranques en una tarde**: con autodeploy, cualquier
merge a `main` recrea el contenedor — **incluido un merge solo-docs, y el de otra persona**. Una hora
de arranque no sobrevive a un repo con varias sesiones mergeando.

Y el fallo mayor estaba debajo: el otro extremo midió «cero filas nuevas» con un SELECT impecable, y
**ese cero no decía nada** — el agente no había recibido ni un turno (`docker logs` desde el arranque:
cero webhooks entrantes). «No emitió» y «no hubo nada que emitir» eran la misma observación, tres veces
seguidas. **Un negativo solo discrimina si el evento buscado PUDO ocurrir**, así que antes de leer un
cero hay que probar que hubo estímulo.

Patrón: **ancla al EVENTO, no al arranque** (la hora del `POST /webhook/...` en el log del productor), y
pásala al que consulta. Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]] ·
[[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]] · [[rebuild-no-recrea-el-contenedor-y-el-sello-de-build-es-ciego-al-reinicio]]
