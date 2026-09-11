---
title: el suelo de un semáforo explica quién entra, no cuánto tarda
date: 2026-09-11
source: facturaia
tags: [rendimiento, gates, medicion, atribucion]
---
Tres hipótesis para explicar un pre-push de 70 min con la máquina a load 17: «contención
de CPU» (load 16,5 real), «el suelo de `fia-gate` nos coló a los dos» (la línea 260 admite
con `running < MIN` **sin mirar `vm.loadavg`**), y «cola por la exclusión mutua de
`KIND=mem`» (línea 259). **Las tres caen contra el log del propio semáforo**: la espera de
admisión MÁXIMA de cualquier rama en 2,5 h fue **1 s**.

La lección es la separación: un semáforo de admisión explica **quién entra**, nunca
**cuánto tarda**. Si la cola mide ~0, la duración está en el trabajo y el semáforo no es
sospechoso — por muy cargada que esté la máquina y por muy real que sea el load.

Y la trampa que produjo un «hueco sin explicar» de 3.700 s: **sumar los `Duration` que
declaran las herramientas y llamar a eso el trabajo**. De 11 etapas del pre-push **solo 2
declaran `Duration`**; se sumaron 3 y el resto quedó invisible. Las que más pesaban no
gastan CPU ni imprimen tiempo: sincronía de migraciones y `gen:types:check`, que hacen RED
contra Supabase. Mide `running→done`, no lo que la herramienta dice de sí misma — y al
agregar por rama, cuidado con mezclar pre-commits con la corrida del push.

Referencia del gate completo de facturaia: **398-419 s limpio, 478 s bajo carga**. Publicar
el suelo como expectativa hace diagnosticar «colgado» donde solo hay contención; el tell
barato es `stat -f %m <log>`. Ver [[el-suelo-de-carga-de-una-maquina-compartida-no-lo-ponen-las-sesiones]].
