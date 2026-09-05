---
title: un project_id local igual al ref de producción hace indistinguibles local y prod
date: 2026-09-06
source: agentesia-crm
tags: [supabase, entornos, produccion, seguridad]
---
`agentesia-crm/supabase/config.toml` tiene `project_id = "kbrtrogwntjmbcqseqhf"`. Eso no es un
nombre: es el **ref del proyecto de producción** de TuCRMIA en Supabase cloud (`tucrmia-prod`, otra
organización). Tres consecuencias, medidas el 6-sep:

- Los contenedores locales se llaman como prod, así que `docker ps` no dice qué estás mirando. Una
  sesión paralela paró ese stack sin saber de quién era y tuvo que preguntar por él.
- El repo está **linkeado** (`supabase/.temp/linked-project.json`, `.temp/project-ref`), así que
  `db reset`, `db push` o `migration up` con `--linked` —o un flag de más— van a la base real.
- `supabase stop` sí es seguro: solo actúa sobre contenedores locales y no admite `--linked`.

**Fix:** el `project_id` de `config.toml` es un NOMBRE (`tucrmia`); el ref del proyecto remoto vive
en `.temp/`, que es su sitio. Y en cualquier repo linkeado, `supabase status` antes de un comando
destructivo: que te confirme que habla del local.
