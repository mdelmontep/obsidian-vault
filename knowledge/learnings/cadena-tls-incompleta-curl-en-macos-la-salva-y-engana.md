---
title: una cadena TLS sin el intermedio funciona en curl de macOS y la rechazan GitHub y node
date: 2026-08-03
source: claude-code-session
tags: [tls, dokploy, webhooks, diagnostico]
---

Un servidor que manda **solo el certificado hoja**, sin el intermedio, es válido para
`curl` en macOS —completa la cadena con los intermedios cacheados del almacén del
sistema— y **es inválido para GitHub y para `fetch` de Node**, que solo usan lo que
el servidor envía.

Efecto real (`dokploymanu.tecnocloud.es`, 3-ago): el webhook de despliegue de GitHub
llevaba **cinco entregas** muriendo con `tls: failed to verify certificate: x509:
certificate signed by unknown authority` y `autoDeploy` no había disparado NUNCA,
mientras desde el Mac todo "funcionaba".

Diagnóstico, no deducción — contar posiciones de la cadena:

```
openssl s_client -connect <host>:443 -servername <host> </dev/null 2>/dev/null \
  | grep -E "^ [0-9] s:|Verify return code"
```

Una sola posición `0 s:` y `Verify return code: 21` = falta el intermedio. Con la
cadena bien: `0 s:` + `1 s:` y `Verify return code: 0 (ok)`. Confirmar con el cliente
que la rechaza: `node -e "fetch('https://host/…')"` → `UNABLE_TO_VERIFY_LEAF_SIGNATURE`.

Fix: servir hoja **+ intermedio**. El intermedio se baja de la URL que la propia hoja
declara en su AIA (`openssl x509 -text | grep "CA Issuers"`) y se verifica **antes** de
instalarlo: `openssl verify -untrusted intermedio.pem hoja.pem` → `OK`.

Ver [[dokploy-guarda-en-su-bd-y-no-toca-el-disco]]
