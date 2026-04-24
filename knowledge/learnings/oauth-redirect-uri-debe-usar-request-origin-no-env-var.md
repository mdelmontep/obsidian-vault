---
title: oauth redirect_uri debe usar request.nextUrl.origin no env var
date: 2026-04-24
source: claude-code-session
tags: [nextjs, oauth, google]
---

En Next.js, el `redirect_uri` de OAuth debe derivarse de `request.nextUrl.origin` en vez de `NEXT_PUBLIC_APP_URL`. Así el mismo código funciona en local (`http://localhost:3000`) y producción (`https://dominio.com`) sin cambiar env vars.

## Patrón

```typescript
// En la API route (connect y callback):
const baseUrl = request.nextUrl.origin

// Pasar a las funciones de OAuth:
generateAuthUrl(state, baseUrl)
exchangeCode(code, baseUrl)

// En el adapter:
function getOAuth2Client(baseUrl?: string) {
  const origin = baseUrl || process.env.NEXT_PUBLIC_APP_URL!
  return new OAuth2Client(clientId, clientSecret, `${origin}/api/auth/google/callback`)
}
```

## Requisitos

- Google Cloud Console debe tener AMBOS redirect URIs registrados:
  - `http://localhost:3000/api/auth/google/callback`
  - `https://dominio-prod.com/api/auth/google/callback`
- Google permite múltiples redirect URIs en la misma credencial OAuth
- El `redirect_uri` del intercambio de tokens DEBE coincidir exactamente con el de la autorización — si no, falla con `redirect_uri_mismatch`
