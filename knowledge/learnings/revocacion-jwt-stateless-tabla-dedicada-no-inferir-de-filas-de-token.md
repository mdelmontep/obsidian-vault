---
title: revocar un jwt stateless antes de exp exige tabla de revocación dedicada, no inferirla de filas de token
date: 2026-06-18
source: claude-code-session
tags: [oauth, jwt, seguridad, supabase]
---

Un access token JWT es **stateless**: válido hasta `exp` sin tocar BD. Para
cortarlo ANTES de `exp` (revocación de grant) el resource server debe consultar
estado en cada request. El claim que ata el token a su grant (p.ej. `gid` = family
del refresh) va FIRMADO dentro del JWT (no forjable).

Anti-patrón detectado en auditoría (MCP TuFacturaIA): inferir "grant revocado" de
la presencia de `revoked_at` en filas de la tabla de **refresh tokens**. Ata la
señal de revocación al ciclo de vida de esas filas → un cron futuro que limpie
refresh expirados borra la señal y un access token revocado **revive** hasta exp.

Fix: **tabla dedicada** (`oauth_revoked_grants(family_id pk, revoked_at, reason)`),
fuente de verdad de `isGrantRevoked`, independiente del refresh. `revokeFamily`
escribe ahí (upsert idempotente). **Inviolable: no cachear `isGrantRevoked`** — la
caché extendería la ventana de revocación a su TTL. Relacionado:
[[signOut-solo-invalida-refresh-no-access-token]].
