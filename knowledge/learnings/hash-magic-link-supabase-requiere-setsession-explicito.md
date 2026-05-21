---
name: hash-magic-link-supabase-requiere-setsession-explicito
description: El hash del magic link Supabase se procesa async; getUser() antes devuelve null y rompe el flow
metadata:
  type: feedback
---

Magic link Supabase (`type=magiclink|invite|recovery`) redirige al `redirect_to` con tokens en hash fragment: `#access_token=...&refresh_token=...&type=magiclink`. El SDK JS detecta el hash y establece sesión, pero **de forma async tras montar**. Si la página llama a `auth.getUser()` al primer render, devuelve null → redirect a /login → user pierde el token aunque era válido.

**Why:** Caso real 2026-05-21 — página `/invitacion` recibía link, JS corría `getUser()` antes de procesar el hash → null → router.replace('/login') → token quemado. Reproducible 100%.

**How to apply:** En toda landing de magic link (`/invitacion`, `/recuperar`, etc.) procesar el hash explícitamente antes de cualquier `getUser`:
```ts
if (typeof window !== 'undefined' && window.location.hash) {
  const params = new URLSearchParams(window.location.hash.slice(1))
  const accessToken = params.get('access_token')
  const refreshToken = params.get('refresh_token')
  if (accessToken && refreshToken) {
    await supabase.auth.setSession({ access_token, refresh_token })
    // Limpiar hash con history.replaceState para que refresh no reprocese token quemado.
    window.history.replaceState(null, '', window.location.pathname + window.location.search)
  }
}
const { data: { user } } = await supabase.auth.getUser() // ahora sí
```
Bonus: detectar también `error=access_denied&error_code=otp_expired` en el hash y mostrar UI "link caducado" en vez del genérico "no encontrado".
