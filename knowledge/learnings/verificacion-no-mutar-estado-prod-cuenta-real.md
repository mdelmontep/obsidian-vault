---
title: scripts de verificación pueden corromper prod si .env.test apunta al proyecto real y la cuenta de test es la tuya
date: 2026-06-23
source: claude-code-session
tags: [ops, tests, supabase, prod]
---
Un script Playwright "contra localhost" sigue usando la BD del `.env.test`. Si `SUPABASE_URL` es el proyecto de PROD y `E2E_EMAIL` es tu cuenta real, cualquier WRITE toca estado compartido y server-side.

Caso real: en una verificación visual el script hizo `switch-org` → cambió `profiles.active_org_id` del usuario real a una org sandbox y de vuelta. Como `active_org_id` es server-side, la sesión EN VIVO del usuario lo reflejó → su bandeja "iba y venía"/salía vacía. Encima el restore usó `.eq('id', userId)` cuando `profiles` se clava por `user_id` → 0 filas, restore silencioso fallido (un UPDATE de 0 filas NO es error).

Reglas:
- Antes de cualquier write en un script de verificación: confirmar que `E2E_EMAIL`/`SUPABASE_URL` no son la cuenta/proyecto reales. Si lo son → solo lectura, o cuenta desechable.
- NUNCA mutar estado server-side de un usuario real (active_org, settings) en tests sobre BD compartida.
- Conocer la PK real (`profiles.user_id`, no `id`) antes de restaurar y verificar el restore con un SELECT.
Ver [[script-one-shot-con-env-local-divergente-de-prod]].
