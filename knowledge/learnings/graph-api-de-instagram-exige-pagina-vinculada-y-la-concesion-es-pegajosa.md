---
title: graph api de instagram exige página vinculada y la concesión de páginas es pegajosa
date: 2026-08-14
source: claude-code-session
tags: [meta, instagram, graph-api, oauth, gotcha]
---
Leer insights de un IG profesional por el flujo clásico (Facebook Login, `graph.facebook.com`)
exige que la cuenta esté **vinculada a una página de Facebook administrada por el usuario del
token**; sin página, la cuenta ni aparece en el picker del OAuth. Y el popup **reutiliza la
selección de la primera autorización sin re-preguntar**: activos nuevos solo entran por «Editar
configuración» del propio popup (la pantalla de Integraciones empresariales no deja tocar páginas).

- «Error validating client secret»: el panel tiene DOS claves (sección Instagram vs Información
  básica); para `oauth/access_token` solo vale la segunda. Aislar el par con
  `grant_type=client_credentials` (sin token de usuario de por medio).
- Tokens del Explorer caducan en 1-2 h; canje `fb_exchange_token` → ~60 días.
- Apps nuevas van por «casos de uso»: insights = «Administrar mensajes y contenido en Instagram»
  (config con login de Facebook, no el de Instagram, que pide rol de tester) + añadir a mano
  `pages_show_list` y `pages_read_engagement` o `/me/accounts` devuelve `[]` con todo «granted».
- Verificación barata E2E: `/me/accounts?fields=instagram_business_account` → `/{ig-id}?fields=username`.
