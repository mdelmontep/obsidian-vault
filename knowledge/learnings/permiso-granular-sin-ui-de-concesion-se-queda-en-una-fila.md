---
title: un permiso granular sin ui de concesión se queda en la fila del que lo creó
date: 2026-08-21
source: facturaia
tags: [permisos, auth, diseño, supabase]
---

Añadir un permiso fino por encima del flag de admin (`superadmin_permissions`
sobre `profiles.is_superadmin`) sin construir a la vez la pantalla para
concederlo deja el reparto en manos de un INSERT manual. Resultado medido en
prod: **1 fila para 7 superadmins**, un año después. Los otros seis ven un 403
en las 52 llamadas que protegen esa clave, y nadie lo reporta como bug del
permiso — lo reportan como «no me deja crear un post».

Agrava: la UI que pinta los botones no consultaba el permiso, así que el 403
aparece al pulsar, no antes.

Fixes, por orden de coste:
- Fila **comodín** `'*'` y consulta `.in('permission_key', [clave, '*'])`:
  cubre las claves futuras, no toca los call sites, no baja la barra a nadie
  más. Ojo al `.limit(1)` ([[supabase-maybesingle-devuelve-null-si-multiples-filas]]).
- O UI de concesión desde el primer día.
- O no añadir el nivel granular: si en la práctica va a tener una fila, es
  `is_admin` con pasos extra (en facturaia ya se bajaron promos y cupones a
  `requireAdmin()` por esto).
