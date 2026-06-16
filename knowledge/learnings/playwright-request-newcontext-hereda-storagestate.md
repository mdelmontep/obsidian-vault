---
title: e2e — request.newContext hereda storageState; multi-org → fijar org activa en el seed
date: 2026-06-16
source: claude-code-session
tags: [playwright, e2e, multi-org, supabase]
---

Dos gotchas en E2E autenticados (caso real `stock-completo.spec.ts` 2026-06-16):

1. `playwright.request.newContext({ baseURL })` HEREDA el `storageState` del proyecto
   (`use.storageState` del config). Un test pensado "sin sesión" sale autenticado y un
   endpoint protegido devuelve datos → el assert de seguridad falla en falso.
   Fix: `newContext({ baseURL, storageState: { cookies: [], origins: [] } })`.

2. Test user MULTI-ORG: la org activa la resuelve `profiles.active_org_id`
   (ver [[rls-multi-org-active-vs-membership]]), no el login. El seeder debe FIJAR
   `profiles.active_org_id` a la org sandbox antes de los tests y RESTAURARLO en teardown;
   si no, la sesión cae en otra org del user y los tests no ven lo sembrado → timeouts.
   Guard: tras sembrar, comprobar vía request autenticado que la sesión ve un id sembrado;
   si no, `test.skip` con diagnóstico en vez de fallar a 20s por test.
