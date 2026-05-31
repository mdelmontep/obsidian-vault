---
title: supabase mfa totp — step-up obligatorio, listFactors solo verified, recovery codes a mano
date: 2026-05-31
source: claude-code-session
tags: [supabase, auth, mfa, 2fa]
---
Integrar 2FA TOTP nativo de Supabase (`auth.mfa.*`). Gotchas:
- `signInWithPassword`/OAuth dejan la sesión en **aal1 aunque exista factor verificado**. Sin step-up explícito (`getAuthenticatorAssuranceLevel` → si `currentLevel==='aal1' && nextLevel==='aal2'` → `challengeAndVerify`) el 2FA es decorativo: el user entra sin 2º factor.
- OAuth NO pasa por la página de login → su step-up hay que forzarlo en middleware redirigiendo a una página intermedia (`/verificar-2fa`). Eximir esa página del propio gate o loop infinito.
- `listFactors().totp` solo trae factores **verified**; los `unverified` colgando están en `.all` → limpiarlos antes de re-enrollar (TS además marca `.totp[].status` como literal `'verified'`).
- `unenroll` exige aal2 (re-verificar el código antes de desactivar).
- Recovery codes NO existen en Supabase y NO elevan AAL → tabla propia de hashes; sirven para desactivar el factor perdido (`admin.mfa.deleteFactor`), no para saltarse el 2FA.
- `session_timeout` por-org NO es posible (JWT expiry global del proyecto) → solo cierre por inactividad client-side. Ver [[2fa-telefono-solo-para-canal-que-lo-usa-no-gate-global]].
