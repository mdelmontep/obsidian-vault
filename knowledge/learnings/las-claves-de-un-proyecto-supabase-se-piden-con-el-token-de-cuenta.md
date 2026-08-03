---
title: las claves de un proyecto supabase se piden con el token de cuenta
date: 2026-08-03
source: claude-code-session
tags: [supabase, credenciales, management-api, metodo]
---

`GET https://api.supabase.com/v1/projects/{ref}/api-keys?reveal=true`, con el PAT de cuenta
como `Bearer`, devuelve la clave **anónima** y la de **servicio** del proyecto. No hace falta
entrar al panel.

Lo que costó: un smoke pasó una noche entera sin ejecutarse, anotado como «bloqueado: la clave
de servicio está en el panel de Supabase y no en 1Password». No estaba bloqueado. El PAT ya
estaba guardado, y es de cuenta, así que alcanza a todos los proyectos.

**La regla, que es lo reutilizable: un bloqueo ANOTADO no es un bloqueo comprobado.** Antes de
escribir «esperando a que alguien me dé X», comprobar si otra credencial que ya tenemos sirve
para pedir X. Un bloqueo inventado cuesta lo mismo que uno real, dura igual, y encima no se ve
porque nadie vuelve a cuestionarlo: queda escrito y se hereda.

Corolario para los ficheros de estado: al anotar un bloqueo, anota **qué se probó**, no solo
qué falta.

Ver [[pooler-supabase-inalcanzable-aplicar-migracion-por-management-api]] ·
[[opsa-service-account-lee-secretos-sin-touch-id]]
