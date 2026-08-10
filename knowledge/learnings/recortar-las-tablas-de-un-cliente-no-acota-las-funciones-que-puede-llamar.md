---
title: recortar las tablas de un cliente no acota las funciones que puede llamar
date: 2026-08-10
source: claude-code-session
tags: [supabase, seguridad, tipos, postgres]
---
Un cliente de Supabase recortado para un panel de administración se construía con
`Omit<Database['public'], 'Tables'> & { Tables: <lista blanca> }`. El `Omit` recorta las tablas y
**conserva `Functions` enteras**, y el `Pick` del cliente incluía `rpc`.

Resultado: cualquier pantalla podía invocar **cualquier función de la base** con la clave de
servicio —que salta RLS— y alcanzar datos de un cliente **sin pasar por la puerta que los registra**.
El recorte de tablas no lo impide: una función lee por dentro las tablas que quiera.

La lección general: **acotar el nombre que se ESCRIBE no acota el alcance de lo que se EJECUTA.**
Una RPC es una puerta lateral a todo el esquema.

Fix: lista blanca de nombres de función, en ejecución y no sólo en el tipo. Y derivarla de su
catálogo en vez de escribirla — repetir el nombre crea un segundo dueño.
Ver [[una-accion-de-servidor-de-next-es-un-endpoint-publico]]
