---
title: una acción de servidor de next es un endpoint público, y el guard del layout no la protege
date: 2026-08-03
source: claude-code-session
tags: [nextjs, seguridad, autorizacion, server-actions]
---

Next le asigna a cada Server Action un identificador y la EXPONE: se invoca con un `POST` y
la cabecera `Next-Action`, **sin pasar por la página**. Así que el guard del `layout.tsx`
protege lo que se PINTA, no lo que se puede LLAMAR. Un panel de administración cuyo layout
comprueba `is_superadmin` y cuyas acciones no, es una ruta que suspende clientes y que sólo
está escondida.

La comprobación va DENTRO de la acción, y no «acordándose» en cada una: envoltorio único
(`accionDeSuperadmin(cuerpo)`) que resuelve el permiso y acuña el `request_id`.

Y NO lo caza ningún test: en una prueba el permiso se inyecta, así que una acción sin
envoltorio y una con un doble permisivo son indistinguibles ejecutando código. Hace falta un
gate ESTÁTICO que compruebe la PROCEDENCIA de cada export del fichero `'use server'` — mismo
argumento que un limitador construido y no enchufado.

Mismo argumento y misma solución que [[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]].
