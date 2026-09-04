---
title: security add-generic-password interactivo trunca el secreto a 128 caracteres
date: 2026-09-05
source: mandadm
tags: [macos, keychain, 1password, opsa, cli]
---
`security add-generic-password -w` sin valor abre un prompt oculto; lo pegado ahí se corta a
**128 caracteres** sin aviso. Un token de cuenta de servicio de 1Password mide ~860, así que
`opsa` fallaba con «unexpected end of JSON input» y el Keychain decía que todo estaba bien.
Fix: no pegar en el prompt. Copiar el token al portapapeles y pasarlo por fichero:
`pbpaste | tr -d '\n' > /tmp/t && security add-generic-password -U -a "$USER" -s op-service-account -w "$(cat /tmp/t)" && rm /tmp/t`.
Comprobar la longitud guardada con `security find-generic-password ... -w | wc -c` antes de culpar al token.
Ver [[cuenta-de-servicio-de-1password-no-ve-bovedas-creadas-despues]].
