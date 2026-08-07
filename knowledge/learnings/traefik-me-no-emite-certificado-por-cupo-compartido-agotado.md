---
title: el cupo de let's encrypt lo agota el dominio compartido, no todos — comprueba el vecino
date: 2026-08-07
source: claude-code-session
tags: [dokploy, tls, dns]
---
`traefik.me` y `sslip.io` resuelven a cualquier IP sin tocar DNS, y Let's Encrypt cuenta cupo **por
dominio registrado**: `traefik.me`, compartido por miles, suele tenerlo agotado. Traefik sirve el
autofirmado y el panel no da error propio.

**Lo que la versión anterior de esta nota concluía mal (2-ago → corregido 7-ago):** metía a `sslip.io`
en el mismo saco y decía «se resuelve con dominio propio». Falso. En el mismo host, `sslip.io` emitía
certificado real de Let's Encrypt desde junio para otra aplicación. Cuatro días de HTTP —y de «sin
datos reales de clientes»— por esa generalización.

**El error de razonamiento, que es lo reutilizable:** «el proveedor no puede» y «nosotros no podemos»
son frases distintas, y la segunda no se deduce de la primera. Se comprueba mirando si algo del mismo
host ya lo hace, y cuesta una línea:

```
echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -issuer
```

Ver [[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]].
