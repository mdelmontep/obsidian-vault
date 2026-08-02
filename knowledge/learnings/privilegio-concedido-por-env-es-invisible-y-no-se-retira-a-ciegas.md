---
title: un privilegio concedido por variable de entorno es invisible, y retirarlo a ciegas revoca en silencio
date: 2026-08-02
source: claude-code-session facturaia
tags: [auth, seguridad, env, infra]
---
`SUPERADMIN_EMAILS` concedía superadmin sin fila en `profiles`. No era un atajo para entrar en el panel: ese mismo booleano permitía, en TODA ruta con sesión, operar contra cualquier organización y saltarse el gate de escritura. O sea lectura y escritura cross-org que **no salía en el panel de miembros y no pasaba por el log de auditoría**, y el proxy solo miraba la BD, así que era invisible justo en la pantalla donde uno iría a buscarlo.

Dos lecciones, y la segunda es la que cuesta tiempo:

1. **Conceder permisos por env los saca del sistema que los audita.** Un `update profiles set is_superadmin` deja rastro y se ve; una variable no hace ninguna de las dos cosas. Si hay que conceder acceso, que sea por el mismo camino que la aplicación sabe enseñar.
2. **No se retira a ciegas.** Borrar la rama revoca en silencio a quien la esté usando, y en producción la variable estaba poblada. El bloqueo era **un dato, no el arreglo**: leer el valor real. Resultó tener dos emails, ambos ya con el flag en BD, así que retirarla no revocó a nadie. Meses de «pendiente» por no haber mirado una variable.

Al retirarla, grep de TODOS los lectores: eran **tres**, no uno. Además de conceder, el panel de miembros la leía por su cuenta para pintar la insignia (`profile?.is_superadmin || env`), así que un test de comportamiento sobre la función de auth no habría detectado que alguien la reintrodujera ahí. El candado tiene que ser también estructural.

Ver [[un-gate-en-el-proxy-vuelve-codigo-muerto-el-gate-del-handler]] · [[defensa-cableada-vs-codigo-muerto]]
