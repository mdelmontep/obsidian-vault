---
title: Next.js unstable_cache no se invalida con escrituras directas a BD desde scripts externos
date: 2026-05-07
source: claude-code-session
tags: [nextjs, caching, gotcha]
---

`unstable_cache(fn, key, { tags: [TAG] })` cachea hasta `revalidateTag(TAG)`. En prod las server actions hacen revalidate y todo va. En dev/scripts:

- Modificar datos via Prisma directo, SQL, seed, o script externo (sin pasar por server action) → el cache **no** se entera.
- El dev server sigue sirviendo el valor cacheado en memoria.

Síntoma: cambias un setting via script, recargas la página, sigues viendo el valor viejo. La BD tiene el valor nuevo. Reinicias dev → ves el valor nuevo.

Fix:
- Reiniciar dev server tras escrituras externas, **o**
- Llamar `revalidateTag(TAG)` desde un endpoint manual.

Pattern para scripts de setup en proyectos Next.js: documentar "tras correr esto, reiniciar pnpm dev" o exponer un endpoint `/api/admin/revalidate?tag=X` con auth.

Caso real: `setup-voice-settings.ts` actualiza `voice_webhook_secret` en `app_settings`, pero `getVoiceSettings()` (cacheado) seguía leyendo el secret viejo en el route handler hasta reiniciar.
