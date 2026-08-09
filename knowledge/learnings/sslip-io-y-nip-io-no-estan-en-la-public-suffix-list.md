---
title: sslip.io y nip.io no están en la Public Suffix List, así que SameSite no protege
date: 2026-08-09
source: claude-code-session
tags: [seguridad, cookies, despliegue, traefik]
---

Desplegar en `<algo>.sslip.io` (o `nip.io`, o `traefik.me`) hace que **cualquiera pueda levantar un
host vecino en ese mismo dominio registrable**. Comprobado con la lista oficial: ninguno de los tres
está en la PSL.

Consecuencias reales, demostradas: un host atacante puede poner `Set-Cookie: …; Domain=sslip.io` y
nuestro servidor la recibe (**fijación de sesión**), y un `<form method=post>` cruzado llega **con la
cookie de la víctima**, porque para el navegador los dos hosts son *el mismo sitio* — o sea que
`SameSite=Lax` deja de valer como defensa CSRF.

**Mitigación sin cambiar de dominio**: nombrar la cookie con prefijo `__Host-`. El navegador solo la
acepta sin `Domain`, con `Secure` y `Path=/`, así que un vecino no puede fabricarla. Ojo: en local
por `http` el navegador la rechaza, así que el nombre debe derivarse de la misma señal que `secure`.

Lo que **no** arregla: verificación de Meta/Google y SPF/DKIM propios. Para eso, dominio de verdad.
