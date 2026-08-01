---
title: capturar un saas para la web pública exige mirar la organización activa
date: 2026-08-01
source: claude-code-session
tags: [rgpd, capturas, marketing]
---
Para enseñar producto en una web pública hace falta entrar en la app, y `app.<dominio>`
redirige a `/login`: sin sesión sólo se captura la pantalla de acceso.

La cuenta buena no es la de producción: en el repo suele haber un `.env.test` con
`E2E_EMAIL`/`E2E_PASSWORD` (guardado en 1Password). Con ella se levanta la app en local
y se captura sin tocar producción.

Pero eso **no basta**: esa cuenta puede tener varias organizaciones y abre en la última
usada. Antes de publicar nada, leer qué pone el selector de organización en la propia
captura. En este caso la primera tanda salió en «Mi empresa» (datos pobres, obra de
demo) y la segunda en «FacturaIA Sandbox» (datos de prueba buenos). Si hubiera abierto
en una org real, la captura llevaría facturas, NIF e importes de clientes a una web
abierta.

Regla: la organización activa se verifica en la imagen, no se supone.
