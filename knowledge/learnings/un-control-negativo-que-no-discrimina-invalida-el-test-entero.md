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

**Variante (10-ago-2026, eje cross-org de TuFacturaIA)**: el control POSITIVO pasaba y aun así la
sonda no servía. La sonda leía el recurso con un id propio (200 ✓) y con uno de otra organización,
esperando 404. Entró como sonda un `GET /clientes/{id}/mandatos`, que es una **colección anidada**:
con un cliente ajeno filtra por `org_id` y devuelve **200 con lista vacía**. El eje cantó 4 fugas
cross-org que no existían. Falta un tercer punto de control, el de la ausencia: pedir la sonda con un
id que **no existe en ninguna parte** y exigir 404. Si ahí responde 200, no distingue «no existe» de
«no es tuyo», y entonces ni su 404 prueba la valla ni su 200 prueba una fuga. Regla corta: una señal
negativa solo prueba algo cuando has descartado que salga por otro motivo.

**Variante (9-ago-2026, `harness-commit-guard`)**: el caso negativo EXISTÍA y pasaba, pero usaba una
forma inofensiva. Probaba que `git diff <ruta>` y `stat <ruta>` no cuentan como escribir en esa ruta
— y la forma que sí se colaba era un `python3` que solo medía mtimes, porque `python3` estaba en mi
lista de «verbos de escritura». Un caso negativo con la forma fácil da la sensación de cubrir la
familia entera. Elige la forma que de verdad se cuela, y confírmalo mutando: la mutación «mencionar =
escribir» tiene que ponerlo rojo. Ver
[[hook-sobre-recurso-compartido-bloquea-a-quien-cierra-no-a-quien-ensucia]].

Instancia 2026-08-18 (arnés de un hook, y el control cazó un **verde falso mío**): cuatro casos nuevos,
el primero «esto NO debe bloquear» → verde. Pero el control «el peligro SÍ bloquea» **también** salió
verde, y eso es imposible: si el peligro no bloquea, la regla no se está armando. Causa: el `cd` estaba
dentro de la función y `$(funcion)` corre en un **subshell**, así que el cwd del test nunca cambiaba y la
regla —que exige estar en `main` de un checkout con worktrees— salía antes de mirar nada. El caso «no
bloquea» pasaba **sin ejercitar nada**.
👉 Regla operativa: en toda suite de guard, el control «el peligro sigue bloqueado» va **en la misma
tanda**, no como extra. Es lo único que distingue «mi exención funciona» de «mi arnés no mide».
