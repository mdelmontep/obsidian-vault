---
title: un trinquete que mide con caché incremental caliente no mide, y sale verde igual
date: 2026-09-07
source: facturaia
tags: [typescript, trinquetes, gates, medicion]
---
Un trinquete de **volumen** (tipos, nodos, líneas) que llama a una herramienta con
caché incremental —`tsc` con `"incremental": true` y su `tsconfig.tsbuildinfo`— no
recorre el programa entero en caliente: devuelve un número minúsculo y da verde a
cualquier cosa. Medido el 7-sep, mismo worktree y commit, 20 min de diferencia:
`types=85` contra `types=1.757.322` en frío, con un tope que discrimina en ~2.000.

Lo perverso: **solo tiene dientes justo después de un cambio grande**, porque un
merge invalida el caché solo. Muerde cuando menos falta hace y calla el resto del
tiempo, y el log imprime `typecheck: OK (types=85)`, que parece una medida.

Fix: borrar el `tsbuildinfo` antes de medir, y un caso que falle si el segundo
número colapsa — sin él, un verde legítimo y uno ciego son idénticos.

**El segundo defecto, y es peor:** si el `tsconfig` incluye ficheros GENERADOS y no
trackeados (`.next/types/**`), el veredicto depende de si alguien levantó el servidor
de desarrollo en ese clon. Medido: 16.794 tipos de diferencia, y tres worktrees del
mismo commit imprimiendo 1.751.145 / 1.760.410 / 1.767.641. Un trinquete solo vale si
su rojo es **accionable**, y nadie escribe los tipos de ruta generados. Separa dos
programas: uno para *¿compila?* (con lo generado, caché a favor) y otro **commiteado**
para *¿cuánto tipo añado?* (sin lo generado, `--incremental false`), y que el script se
niegue a arrancar si el segundo falta en vez de caer al primero en silencio.
Regenera el baseline en el mismo PR: si cambia el programa medido y no el tope, el
trinquete queda flojo por la diferencia exacta.

Corolario al cruzar el tope de verdad: **baja tu propio coste antes de subir un
baseline compartido**. 821 literales de objeto contra una interfaz costaban 2.710
tipos; el mismo fichero generado como `readonly string[]` + `.map()` cuesta plano.
Ver [[antes-de-exceptuar-una-deuda-mira-que-trinquete-la-mide]].
