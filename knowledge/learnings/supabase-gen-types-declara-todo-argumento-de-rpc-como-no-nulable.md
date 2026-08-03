---
title: supabase gen types declara todo argumento de rpc como no nulable; el default lo hace opcional
date: 2026-08-03
source: claude-code-session
tags: [supabase, typescript, postgres, rpc]
---

`supabase gen types typescript` emite los argumentos de una función como `p_x: string` aunque
la función acepte NULL: el catálogo de Postgres no guarda esa información. Resultado: el
llamante que legítimamente pasa `null` **no compila**, y la salida evidente es
`valor as string` — un cast que sigue en verde el día que la condición se invierta.

Se arregla en la FIRMA, no en el llamante: con `DEFAULT NULL` el generador lo emite como
`p_x?: string`, y con `exactOptionalPropertyTypes` decir «no hay valor» pasa a ser **omitir la
clave**, que es lo que significa:

```ts
...(actor !== null ? { p_actor_user_id: actor } : {})
```

Gotcha: en Postgres los parámetros con default van AL FINAL, así que suele haber que
reordenar → cambia la firma → hace falta `DROP FUNCTION` explícito antes del
`CREATE OR REPLACE`, o queda una sobrecarga fantasma y cualquier llamada con argumentos
nombrados falla con `42725` ambiguo.
