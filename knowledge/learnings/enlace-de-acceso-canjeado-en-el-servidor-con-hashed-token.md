---
title: el action_link de Supabase resuelve la sesión en el navegador; hashed_token la resuelve en el servidor
date: 2026-08-03
source: claude-code-session
tags: [supabase, auth, next, seguridad, ssr]
---
`POST /auth/v1/admin/generate_link` devuelve dos cosas y no dan lo mismo:

- **`action_link`** apunta a `/auth/v1/verify` de Supabase, que verifica y redirige con la sesión en el
  **fragmento** (`#access_token=…`). Un fragmento solo lo lee JavaScript: la sesión se resuelve en el
  cliente y el token pasa por el historial del navegador.
- **`hashed_token`** permite construir tu propia URL (`/auth/callback?token_hash=…&type=magiclink`) y
  canjearla en el SERVIDOR con `verifyOtp`. La sesión sale en cookies `HttpOnly` que ningún script de la
  página puede leer, y el enlace apunta a tu dominio, que es lo que alguien reconoce antes de pulsar.

Parsear `type` contra una lista cerrada propia: `verifyOtp` admite más tipos de los que emites, y pasarle
el valor crudo de la URL convierte un enlace manipulado en una excepción de la librería.

Ver [[supabase-mint-access-token-sin-password-via-generate-link]] ·
[[magic-link-un-solo-uso-lo-preconsumen-escaneres-email]]
