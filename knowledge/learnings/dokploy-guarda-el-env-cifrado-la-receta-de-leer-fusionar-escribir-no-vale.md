---
title: dokploy guarda el env CIFRADO — leer-fusionar-escribir no vale, usa huellas para probar la reconstrucción
date: 2026-08-07
source: claude-code-session
tags: [dokploy, secretos, infra]
---
`application.update` **reemplaza el bloque `env` entero**, así que la regla es leer, fusionar y escribir.
Pero desde un agente esa lectura no existe por dos lados a la vez:

- `application.one` devuelve el env en claro → el wrapper obligatorio lo **borra** antes de imprimir.
- Su propia base de datos lo guarda **cifrado**: 460 caracteres sin un solo `=`.

**Lo que sustituye a la lectura es una prueba, no una suposición.** Se reconstruye el bloque entero
desde la fuente local y, antes de escribir, se compara la **huella SHA-256 de cada variable que ya vive
en el contenedor** (`docker exec … printenv`, por SSH) contra la de tu fichero. Si coinciden byte a
byte, reconstruir no puede perder nada — que es lo que la regla pedía de verdad.

Todo el guion corre **en el host** y sólo imprime nombres, longitudes y huellas: ningún valor cruza a la
sesión. Después, verificar en el plano de datos (`printenv` en el contenedor nuevo), nunca en el de
control: en Dokploy, 200 y releer no significan aplicado. Y el contenedor no toma el cambio al vuelo.
