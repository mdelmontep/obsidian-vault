---
title: una verificación que inicializa si falta es tautológica sobre el estado vacío
date: 2026-09-21
source: agh-iberica
tags: [verificacion, prod, secretos, canario, metodo]
---
AGH 21-sep. El canario de la clave de cifrado de RRHH (`checkHrKeyCanary`) hace dos cosas según el estado: **si hay fila, descifra y compara**; **si no la hay, cifra con la clave cargada y la inserta**. Usarlo como sonda de «¿la clave de prod es la buena?» solo prueba algo en la primera rama. Sobre una base sin fila, la función **firma el canario con la misma clave que se quería verificar** y devuelve `ok`: una verificación que no puede fallar.

**Patrón:** toda función «comprueba o inicializa» (canarios, bootstrap de admin, checksums de migración, `ensureX`) es un instrumento válido solo si el estado ya existe. Antes de usarla para verificar:
1. confirma por separado que el estado está (`SELECT count(*) … WHERE key_version = N`);
2. haz que la sonda **aborte** si no está, en vez de dejar que lo cree;
3. usa el código del repo, no una reimplementación de la cripto: si derivas la clave distinto, la sonda da un falso `wrong_key`, que es el peor resultado.

Con eso, la sonda es de solo lectura y discrimina. Resultado ese día: `ok`. Hermano: [[verificar-una-clave-de-firma-en-prod-ejercitando-el-flujo-no-el-health]] (ejercer el flujo, no el health).
