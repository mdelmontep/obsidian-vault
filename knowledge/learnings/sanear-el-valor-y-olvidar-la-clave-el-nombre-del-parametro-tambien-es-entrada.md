---
title: sanear el valor y olvidar la clave, porque el nombre del parámetro también es entrada
date: 2026-07-29
source: claude-code-session
tags: [seguridad, agentes, prompt-injection, facturaia]
---

Escribí un saneador de URLs con allow-list: de los parámetros conocidos se guarda nombre y valor,
del resto solo el nombre. Y apliqué la redacción de secretos a la ruta y al valor... **nunca al
nombre**. Resultado: `?ana.perez@acme.com` y `?eyJhbGciOi…` se guardaban literales, porque nadie
espera un secreto en la posición de la clave. Si tu esquema tiene dos posiciones, ambas son entrada
del usuario.

Segundo hueco del mismo módulo: **no neutralizaba caracteres de control**. `?tab=x%0A%0AInstruccion: …`
se guardaba con saltos de línea REALES, y ese campo acaba en la cabecera del prompt de un agente que
corre con `--dangerously-skip-permissions` y un token de repo. Un salto de línea ahí parece una
instrucción nueva. En ese fichero la descripción del usuario sí iba vallada entre comillas y la
página no: **el campo que nadie considera "texto libre" es mejor canal de inyección que el que sí lo
es**, porque solo se valla lo que parece peligroso.

Regla: todo campo que llegue a un prompt va (1) con controles colapsados, (2) vallado, y (3) con la
redacción aplicada a TODAS sus posiciones. Y ojo al cambio que amplía la alcanzabilidad sin tocar el
saneador: pasar de `pathname` a `pathname+search` convirtió esto en "mándale un enlace y ya".

Ver [[orden-imposible-en-su-entorno-el-agente-explora-hasta-que-lo-matan]]
