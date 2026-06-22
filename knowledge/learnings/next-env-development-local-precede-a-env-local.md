---
title: .env.development.local precede a .env.local en next (qa local sin tocar prod)
date: 2026-06-22
source: claude-code-session
tags: [nextjs, env, supabase, qa]
---

`@next/env` carga los .env en este orden y **solo fija una clave si no estaba ya
definida** (la primera que la define gana):

1. variables exportadas en el shell (process.env) — ganan sobre TODO
2. `.env.$NODE_ENV.local` (p.ej. `.env.development.local`)
3. `.env.local`
4. `.env.$NODE_ENV` → `.env`

Consecuencia útil: para QA de una app Next contra una BD/Supabase **local** sin
tocar el `.env.local` de prod (que tiene credenciales reales y NO se debe
clobberar), crear un `.env.development.local` con SOLO los overrides locales
(`NEXT_PUBLIC_SUPABASE_URL`, anon/service keys, `SUPABASE_DB_URL`…). Gana sobre
`.env.local`, el resto de claves caen a `.env.local`. Está gitignored. Borrarlo al
terminar. Confirmar en el banner de arranque: `Environments: .env.development.local, .env.local`.

Verificado leyendo el source de `@next/env` (Next 16). NO fiarse de la memoria:
"this is NOT the Next.js you know".
