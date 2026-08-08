---
title: un aserto por subcadena sobre stdout+stderr lo cumple el propio mensaje de error
date: 2026-08-08
source: claude-code-session
tags: [tests, metodo, hooks, bash, jq]
---

Suite de un hook que captura la salida con `2>&1` y afirma `grep -q "sin empujar"`. Muté el hook
desbalanceando una llave: `jq` falló y, como los errores de compilación de `jq` **imprimen el
programa entero**, el mensaje de error contenía la frase buscada. El test pasó **con el hook roto**, y
el mutante sobrevivió — que es lo que hizo visible el problema, porque leyendo el test no se ve nada.

Es un falso verde de la familia de [[asercion-de-ausencia-necesita-fixture-que-pueda-fallar]], con
otro mecanismo: ahí el fixture no puede producir la señal; aquí **el fallo produce la señal**.

Fix: el aserto no va sobre el texto, va sobre la **estructura parseada**. Primero «¿es JSON válido?»
—si no, el test falla ahí— y luego se leen los campos (`.decision`, `.reason`) con `jq -e`. De paso
distingue «no bloquea» de «petó», que con `grep` son indistinguibles.

Generalizable a cualquier CLI que devuelva JSON/XML: si mezclas `2>&1` en la variable que asertas, la
salida de error entra en el mismo saco que la buena. O separas los flujos, o validas el formato antes
de buscar dentro.

**Y el meta-aprendizaje, tres veces en la misma sesión**: el arnés de verificación mintió tres veces
(un bucle que pulsaba siempre el primer elemento, un `startsWith` que confundía dos columnas, y esto).
Un verde solo vale si has matado un mutante con él. Ver
[[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
