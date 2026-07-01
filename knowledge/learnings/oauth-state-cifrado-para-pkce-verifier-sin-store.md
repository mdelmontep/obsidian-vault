---
title: oauth authorization-code sin store de sesión — sella el pkce verifier en un state cifrado
date: 2026-07-02
source: claude-code-session
tags: [oauth, pkce, seguridad, csrf]
---

OAuth authorization-code + PKCE en backend **sin store de sesión** entre `/authorize` y
`/callback`: mete el `code_verifier` dentro del parámetro `state`, pero **cifrado** (AES-256-GCM),
no solo firmado con HMAC. El verifier debe viajar **confidencial** por el navegador; un state
solo-firmado lo expondría en claro y rompería PKCE.

Payload del state: `{ tenantId, userId, codeVerifier, nonce, exp }` → base64url. GCM ya
autentica (tampered → no abre), el `nonce` lo hace único y el `exp` lo hace no-replayable.
Así el state no necesita registro externo de nonces consumidos para el MVP.

Cierra CSRF + authorization-code injection aunque el callback y el `client_id` sean públicos:
un `code` filtrado es inútil sin el verifier, que nunca sale del server en claro.
Claves de cifrado y de firma: derivar por HKDF de una master (dominio separado), no reusar cruda.
