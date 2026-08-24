---
title: un semáforo que envuelve un comando que vuelve a pedirle slot se interbloquea consigo mismo
date: 2026-08-24
source: facturaia
tags: [harness, concurrencia, git-hooks, gates]
---
Un semáforo de slots (`fia-gate`) empezó a clasificar `git push` como trabajo pesado y a
retenerle un slot durante toda la orden. Pero el `pre-push` del repo **vuelve a llamar al
semáforo** para la suite y el build, hereda el tipo de slot por entorno, y la exclusión mutua
se lo niega **porque lo tiene su propio padre**. Padre e hijo peleándose por el mismo slot:
abrazo mortal en todos los push de la máquina.

Se diagnostica mal porque el hook tiene un mensaje preparado para el watchdog, así que el
hijo muere a los 900 s y **se ve como un fallo de tests**, no como un interbloqueo.

Regla: si envuelves un comando que en su cadena puede volver a invocarte, necesitas **marca de
reentrancia** — el que coge slot exporta una marca y el anidado corre en línea sin pedir slot,
ya está contabilizado por su ancestro. Y la marca debe llevar **identidad, no solo existencia**:
comprobar que el directorio del slot existe no prueba que sea el de tu ancestro, porque los
slots se reciclan por índice y un huérfano con la marca puesta se colaría entero.

Ninguna suite que solo mida clasificación lo caza: ahí la clasificación es correcta. El caso
que discrimina es padre-pesado con hijo-pesado, y hay que lanzarlo de verdad.
Ver [[un-resultado-vacio-no-es-un-hecho-hasta-que-miras-el-exit-code]].
