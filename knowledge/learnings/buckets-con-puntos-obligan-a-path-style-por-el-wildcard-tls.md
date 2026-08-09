---
title: un bucket S3 con puntos en el nombre obliga a path-style por el comodín del certificado
date: 2026-08-09
source: claude-code-session
tags: [s3, wasabi, tls, gotcha]
---
`cliente.dominio.com.s3.eu-west-2.wasabisys.com` falla con `ERR_TLS_CERT_ALTNAME_INVALID`
antes de firmar nada: el certificado de Wasabi cubre `*.s3.<region>.wasabisys.com`, y un
comodín TLS cubre **un solo nivel**. Si el bucket lleva puntos —y los de la casa los llevan,
porque van nombrados por dominio— el estilo virtual-host es inalcanzable.

Fix: path-style (`https://s3.<region>.wasabisys.com/<bucket>/<clave>`), que además es lo que
firman igual todas las herramientas. En AWS real pasa lo mismo con buckets con puntos.

Señal para reconocerlo rápido: el error es de TLS, no de S3 — no llega ni a haber respuesta
HTTP que leer.
