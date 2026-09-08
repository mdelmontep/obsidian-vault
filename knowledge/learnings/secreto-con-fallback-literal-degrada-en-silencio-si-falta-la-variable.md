---
title: un secreto con fallback literal deja el webhook abierto sin que nada falle
date: 2026-09-08
source: centro-elphis
tags: [seguridad, n8n, webhooks, secrets]
---

Patrón encontrado en 5 webhooks: `const esperado = $env.RETELL_WEBHOOK_SECRET || 'literal-de-desarrollo'`.
Ninguna de las variables existía en el contenedor, así que **el secreto efectivo era el literal
escrito en el workflow**: cualquiera con acceso de lectura al workflow tiene la llave, y el
sistema no da ninguna señal de estar degradado — los 401 siguen saliendo, las pruebas pasan,
el endpoint parece autenticado.

Un `||` es una decisión de diseño invisible: convierte "falta el secreto" en "usa este otro",
que es justo lo contrario de lo que se quiere en producción. El fallback debe ser fallar
ruidosamente (o bloquear), nunca un valor por defecto que funcione.

Comprobación, sin imprimir nada: `docker exec <c> sh -c 'for v in A B C; do eval x=\$$v; [ -z "$x" ] && echo "$v AUSENTE" || echo "$v len=${#x}"; done'`.
Ver [[compose-que-enumera-variables-no-entrega-lo-que-guardas-en-el-panel]].
