---
title: qa de páginas server-component con playwright = inyectar la cookie de @supabase/ssr, no hacer login por ui
date: 2026-06-18
source: claude-code-session
tags: [playwright, supabase, nextjs, e2e, qa]
---

En el **dev server** (Turbopack) bajo Playwright headless la hidratación puede no prender: el `<form onSubmit={preventDefault}>` del login hace **submit nativo** (la URL queda en `/login?`, sin cookies) y nunca llega a firmar. Esperar más (`waitForTimeout`, `networkidle`) no lo arregla.

Para QA de una página **server-component** (solo necesita la cookie legible en servidor) NO pelees con el login UI: fírmate server-side y captura la cookie exacta que pondría el browser:

```ts
const jar = {}
const sb = createServerClient(URL, ANON, { cookies: {
  getAll: () => Object.entries(jar).map(([name,value])=>({name,value})),
  setAll: (l) => l.forEach(({name,value})=>{ jar[name]=value }) } })
await sb.auth.signInWithPassword({ email, password })   // jar = cookies a inyectar
await ctx.addCookies(Object.entries(jar).map(([name,value])=>({name,value,domain:'127.0.0.1',path:'/'})))
```

Cookie = `sb-<ref>-auth-token`, `ref = new URL(supabaseUrl).hostname.split('.')[0]` (local → `sb-127`). Relacionado: [[playwright-domcontentloaded-no-espera-hidratacion-rsc]], [[supabase-mint-access-token-sin-password-via-generate-link]].
