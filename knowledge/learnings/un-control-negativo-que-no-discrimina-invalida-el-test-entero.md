---
title: mide el control negativo ANTES de escribir un test de verificación — si no discrimina, mide el instrumento
date: 2026-08-06
source: claude-code-session
tags: [testing, verificacion, tts, metodo]
---
Iba a montar un round-trip para verificar que el agente dice bien un teléfono:
`texto → TTS → audio → STT → ¿vuelven los 9 dígitos?`. Antes de escribirlo medí el
**control negativo** (el string crudo, como sonaba antes del fix):

```
"…comercial, 617314938, como contacto…"          → vuelve "617-314-938"
"…comercial, seis uno siete, tres uno cuatro…"   → vuelve "617-314-938"
```

Idénticos. Ese TTS ya leía el número crudo dígito a dígito: **nunca tuvo el bug**, así
que el test no podía ponerse rojo por el motivo que importa — medía la normalización
del STT, no mi string. Habría sido cobertura aparente, y de las peores: verde, cara y
convincente.

Regla: en cualquier arnés de verificación (round-trip, sonda, canario), **correr primero
la versión ROTA**. Si pasa, el instrumento no sirve para esa pregunta. Y si el motor bajo
prueba no es el de producción, el test mide una propiedad distinta — dilo dentro del
fichero. Ver [[el-fallo-real-no-era-acustico-era-un-camino-sin-cablear]].

**Variante (9-ago-2026, `harness-commit-guard`)**: el caso negativo EXISTÍA y pasaba, pero usaba una
forma inofensiva. Probaba que `git diff <ruta>` y `stat <ruta>` no cuentan como escribir en esa ruta
— y la forma que sí se colaba era un `python3` que solo medía mtimes, porque `python3` estaba en mi
lista de «verbos de escritura». Un caso negativo con la forma fácil da la sensación de cubrir la
familia entera. Elige la forma que de verdad se cuela, y confírmalo mutando: la mutación «mencionar =
escribir» tiene que ponerlo rojo. Ver
[[hook-sobre-recurso-compartido-bloquea-a-quien-cierra-no-a-quien-ensucia]].
