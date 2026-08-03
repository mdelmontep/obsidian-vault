---
title: un replay que arranca más limpio que producción es ciego, y su verde se cita como prueba
date: 2026-08-03
source: claude-code-session
tags: [postgres, supabase, migraciones, gates, testing, docker]
---
Si el Postgres desechable nace sin los privilegios por defecto del proveedor, el ACL final del replay
coincide con lo que la migración escribe. En producción no: es la **resta** entre lo que ya había y lo
que la migración revoca. Toda esa clase de fallo es invisible, y el verde se cita como evidencia.

Caso real: doce asserts de privilegios en verde mientras `TRUNCATE` estaba concedido en las doce tablas
de producción ([[truncate-salta-rls-y-sobrevive-al-revoke-de-update-y-delete]]). Al añadir al bootstrap
el `alter default privileges` real de Supabase, el replay se puso rojo a la primera.

Regla: todo supuesto del proveedor que el entorno de pruebas imite se copia de una **lectura real del
catálogo** (`pg_default_acl`, con la fecha en el comentario), no de la documentación ni de memoria.

Corolario general: un entorno de pruebas más limpio que el de verdad no es «casi igual», es ciego.
