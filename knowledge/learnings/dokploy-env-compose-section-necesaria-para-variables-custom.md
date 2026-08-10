---
title: dokploy env custom necesita estar en compose environment: además del panel
date: 2026-06-02
source: claude-code-session
tags: [dokploy, docker, n8n, infra]
---

Var en panel Dokploy + Deploy no basta si el compose no la referencia explícitamente.
El panel genera un `.env` para sustitución `${VAR}` en el compose, pero solo las
vars listadas en `environment:` del servicio entran al container.

Fix: añadir `- NOMBRE_VAR=${NOMBRE_VAR}` en la sección `environment:` del servicio
en el compose panel → guardar → Deploy.

Verificar con `docker exec <container> env | grep VAR`, nunca confiando en el panel.

Diagnóstico rápido desde n8n: en un Code node añadir temporalmente
`try { val = $env.VAR } catch(e){ val = '__ERR__' }` y retornar el valor.
`''` = var ausente en container (catch silenciado). `__ERR__` = bloqueo de acceso.

Caso 2026-06-02 Elphis: `ELPHIS_NOTIF_RECEPCION` visible en panel pero `''` en
runtime. `ELPHIS_NOTIF_INGRESO` sí funcionaba porque fue añadida en sesión anterior
donde también se editó el compose. Dos deploys sin efecto hasta añadir la línea.

Segundo modo de fallo, más tonto y más frecuente (10-ago, mismas vars): **Deploy sin Save
previo sale VERDE sin aplicar nada** («Compose deployed successfully», 0s). El panel no
persiste los cambios de Environment al navegar a otra pestaña. El tell no es el toast: es
que el container **no se recrea**. Si sigue en `Up 3 days`, no se aplicó nada.
Gate real, en este orden: `grep NOMBRE /etc/dokploy/compose/<stack>/code/.env` → uptime del
container → `docker exec <container> printenv NOMBRE`. Y ojo: ese `.env` de disco lo regenera
el panel, editarlo a mano no sirve.

Hermano de [[dokploy-env-clave-dos-puntos-no-se-parsea]].
