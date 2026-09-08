---
title: ccEmail fuera de options en el nodo email de n8n se descarta sin dar error
date: 2026-09-09
source: clinica-zen
tags: [n8n, email, smtp, gotcha]
---
En `n8n-nodes-base.emailSend` typeVersion **2.1** el CC va dentro de `options`.
Puesto en la RAÍZ del nodo (`{ toEmail, ccEmail, subject, html }`) el nodo no se
queja, no avisa y **manda el correo sin copia**: el parámetro simplemente no
existe a ese nivel y se ignora. Sobrevive a revisiones porque leyendo el JSON
parece correcto y el envío sale en verde.

Se ve en la SALIDA del nodo, que es lo único que no miente: `accepted` lista las
direcciones que el SMTP aceptó de verdad.
- raíz →    `"accepted": ["destino@x.es"]`
- options → `"accepted": ["destino@x.es", "copia@y.es"]`

En Clínica Zen el CC a `info@zendental.es` llevaba así desde que se puso: la
clínica no recibió copia de ninguna confirmación. Al auditar un envío, comparar
`accepted` contra los destinatarios esperados; un `sent: true` no dice a quién.
Mismo patrón que [[n8n-alwaysoutputdata-en-un-if-inyecta-item-vacio-y-dispara-alertas-falsas]]: en n8n, un
parámetro en el nivel equivocado es un no-op silencioso.
