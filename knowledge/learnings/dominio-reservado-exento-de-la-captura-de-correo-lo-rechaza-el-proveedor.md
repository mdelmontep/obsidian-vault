---
title: exceptuar example.com de la captura de correo no lo entrega, lo rechaza el proveedor
date: 2026-08-03
source: claude-code-session
tags: [email, resend, facturaia, entornos-de-prueba]
---
Al montar captura de correo saliente para orgs de prueba (redirigir a un buzón en
vez de escribir a personas reales) es tentador exentar los «sumideros»
—`example.com`, `test.com`— con el argumento de que no son personas. Falso con
Resend: los rechaza en origen con `Invalid \`to\` field. Please use our testing
email address instead of domains like \`example.com\``.

O sea que la excepción no los deja pasar: los convierte en un **fallo de envío
garantizado**. Y si hay un cron que reintenta a diario (recordatorio de cobro),
eso es una fila `failed` nueva cada día y una incidencia «N emails con error en
24h» que no se cierra nunca.

Regla: a la lista de exentos van solo direcciones que el proveedor **acepta de
verdad** (en Resend, `delivered@resend.dev` y sus hermanas `bounced@`/
`complained@`). Los dominios reservados RFC 2606 se capturan como cualquier
externo. Verificarlo mirando `email_log`, no razonando sobre el dominio.

Caso: TuFacturaIA PR #1492.
