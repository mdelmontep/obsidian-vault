---
title: rls policy que subconsulta su propia tabla → recursión 42P17
date: 2026-06-10
source: claude-code-session
tags: [supabase, postgres, rls, security]
---

Una política RLS con `(SELECT ... FROM <tabla>)` en su `USING`/`WITH CHECK`,
donde `<tabla>` es la MISMA que protege, lanza al evaluarse:
`42P17: infinite recursion detected in policy for relation "<tabla>"`.

Caso real TuFacturaIA (mig 240): `profiles_update` hacía anti-escalada con
`WITH CHECK (is_superadmin = (SELECT is_superadmin FROM profiles WHERE
user_id = auth.uid()))`. Latente porque ningún flujo cliente hacía UPDATE de
profiles con RLS activa (el resto usa service_role, que bypasa RLS); el primer
UPDATE cliente (guardar `dashboard_config`) devolvía HTTP 500.

Fix: función `SECURITY DEFINER STABLE` que lee la columna con bypass de RLS;
la policy compara contra esa función. `REVOKE EXECUTE FROM PUBLIC, anon`
(conservar `authenticated`: la policy la evalúa con ese rol). Ver
[[supabase-rpc-security-definer-execute-public]].
