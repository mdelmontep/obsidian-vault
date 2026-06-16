---
title: supabase storage rest (subir/borrar) con keys sb_secret_ exige apikey + authorization
date: 2026-06-16
source: claude-code-session
tags: [supabase, storage, api]
---

Al usar la **Storage REST API** directamente (no el SDK) con las nuevas keys
`sb_secret_…` (formato corto, ~40 chars, no el JWT largo):

- `POST/DELETE /storage/v1/object/<bucket>/<path>` necesita **AMBOS** headers:
  `Authorization: Bearer <sb_secret>` **y** `apikey: <sb_secret>`.
- Con solo `Authorization` devuelve **400** (no 401), lo cual despista: parece
  body malformado cuando en realidad es auth incompleta.
- El SDK js mete los dos headers solo; al hacer curl/fetch a mano hay que ponerlos.

Caso: smoke "Resolver con Claude" subiendo una captura al bucket
`feedback-screenshots` — 400 hasta añadir `apikey`.
