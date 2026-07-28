---
title: un proceso que agota su cuota puede salir con exit 0 y hacerse pasar por "no había nada que hacer"
date: 2026-07-28
source: claude-code-session
tags: [runner, headless, cuotas, observabilidad, falsos-negativos]
---

Un orquestador que juzga el resultado por el **exit code** más el estado del árbol se traga el peor fallo posible: el proceso agota la cuota, sale con **0**, no toca ningún fichero, y el orquestador lo cierra como "terminó y decidió no cambiar nada". En verde. El mensaje del límite acababa además publicado como diagnóstico técnico en el hilo del ticket del cliente.

Reglas que salen de ahí:

- **Un árbol limpio no significa "no había trabajo"**. Antes de dar por bueno un "sin cambios", clasificar la salida.
- Clasificar por **texto de stdout Y stderr**: el error fatal de `claude` sale por stdout, no por stderr.
- Con exit 0, mirar solo la **cola** de la salida (~800 chars): si no, un diagnóstico que mencione "usage limit reached" se clasifica como cuota agotada.
- El patrón de texto no es contrato estable: aislarlo en una constante, y que un falso negativo degrade al comportamiento anterior, nunca a un éxito falso.

Caso real 2026-07-28, TuFacturaIA (#1307). Ver [[el-limite-de-uso-de-claude-es-de-organizacion-no-de-cuenta]].
