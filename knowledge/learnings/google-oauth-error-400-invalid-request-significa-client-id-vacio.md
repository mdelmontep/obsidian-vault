---
title: google oauth error 400 invalid_request significa client_id vacío
date: 2026-04-24
source: claude-code-session
tags: [google, oauth, facturaia]
---

Cuando Google devuelve error 400 `invalid_request` con `flowName=GeneralOAuthFlow`, es porque `client_id` llega vacío o undefined al construir la URL de autorización.

## Causa raíz

El código pasa `process.env.GOOGLE_CLIENT_ID` al `OAuth2Client` de `google-auth-library`, pero la variable no existe en `.env.local`. Google recibe `client_id=undefined` y rechaza la request.

## Diagnóstico rápido

1. Verificar que `.env.local` tiene `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET`
2. Reiniciar dev server después de añadir las variables
3. En Google Cloud Console, verificar que el redirect URI coincide exactamente con el que genera el código

## Contexto

- Librería: `google-auth-library` v10.x
- Framework: Next.js (App Router)
- El error no menciona "client_id" — solo dice "invalid_request", lo que despista
