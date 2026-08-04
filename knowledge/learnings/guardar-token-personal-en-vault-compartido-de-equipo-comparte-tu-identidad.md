---
title: guardar un token personal en el vault compartido del equipo lo comparte de facto
date: 2026-08-04
source: claude-code-session
tags: [1password, seguridad, onboarding, credenciales]
---
Al dar de alta a dos colaboradores nuevos, generé mi `SUPABASE_ACCESS_TOKEN` personal (Management
API, nivel de cuenta) y lo guardé en el mismo vault de 1Password recién compartido con ellos para
las claves del proyecto (`anon`/`service_role`). Efecto: cualquiera con acceso al vault podía
actuar con mi identidad en la Management API — sin trazabilidad de quién hizo qué, y sin poder
revocárselo a uno sin invalidármelo a mí también.

**La regla**: un vault de equipo es para credenciales DEL PROYECTO (compartidas por diseño); un
token de acceso personal va al vault privado de quien lo genera, nunca al compartido — aunque
"guardarlo donde está todo lo demás del proyecto" parezca lo ordenado.

Se detectó por revisión manual antes de invitar a nadie al vault, no por ningún gate.

Ver [[las-claves-de-un-proyecto-supabase-se-piden-con-el-token-de-cuenta]]
