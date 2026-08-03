---
title: en dokploy un 200 y una relectura correcta no significan aplicado
date: 2026-08-03
source: claude-code-session
tags: [dokploy, despliegue, verificacion]
---

La API de Dokploy escribe en **su base de datos**, no en el disco del servidor. La
consecuencia es un modo de fallo que parece imposible: `certificates.update` devolvió
**200**, releer confirmó los dos bloques PEM guardados, y **Traefik siguió sirviendo el
certificado viejo durante horas**. El arreglo estaba guardado y era INERTE.

Lo materializa una recarga: `settings.reloadTraefik` / `settings.reloadServer` (unos
segundos de 502 en el host — avisar antes si es compartido).

No es un caso aislado, es el patrón de esta API:
- `application.saveEnvironment` responde **200 con cuerpo vacío y no guarda nada**; el
  que funciona es `application.update`.
- La escritura de entorno **reemplaza el bloque entero**: leer, fusionar, escribir.
- Los nombres de endpoint no son adivinables (`certificates.all` en plural existe,
  `certificate.all` da 404). Tantear con `POST {}`: 400 = existe y valida, 404 = no existe.

Regla: **verificar en el plano de datos, nunca en el de control.** `openssl s_client`,
`docker exec <c> env`, una llamada que devuelva el efecto. "Guardado" y "aplicado" son
dos cosas, y releer solo prueba la primera.

Ver [[cadena-tls-incompleta-curl-en-macos-la-salva-y-engana]] ·
[[verificar-deploy-de-env-por-comportamiento-no-por-contenedor-recreado]]
