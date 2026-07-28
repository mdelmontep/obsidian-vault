---
title: el límite de uso de Claude es de ORGANIZACIÓN, cambiar de cuenta dentro de la misma org no desbloquea
date: 2026-07-28
source: claude-code-session
tags: [claude-code, cuotas, runner, harness, dokploy]
---

Cuando un runner headless (`claude -p`) agota la cuota, el CLI imprime:

> `You've hit your org's monthly spend limit · ask your admin to raise it at claude.ai/settings/usage`

La palabra clave es **org's**. El tope es de la organización de Claude, no del usuario, así que dar de alta un segundo token OAuth (`claude setup-token`) de otra cuenta **de la misma org** vuelve a chocar con el mismo muro. Antes de montar multi-cuenta, comprobar en `claude.ai/settings/usage` si las cuentas están en organizaciones distintas; si no lo están, lo que hay que subir es el límite de la org.

Corolario de diseño: si el runner elige cuenta por configuración, que registre **qué cuenta usó** en el error y en el log. Sin ese dato, "falló por cuota" no distingue entre "esta cuenta está agotada" y "toda la org lo está", que llevan a acciones opuestas.

Caso real 2026-07-28, runner "Resolver con Claude" de TuFacturaIA. Ver [[proceso-que-agota-la-cuota-puede-salir-con-exit-0-y-parecer-sin-cambios]].
