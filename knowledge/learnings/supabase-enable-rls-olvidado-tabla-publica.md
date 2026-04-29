---
title: supabase: policies sin ENABLE ROW LEVEL SECURITY = tabla pública
date: 2026-04-29
source: claude-code-session
tags: [supabase, rls, seguridad]
---

Puedes tener políticas CREATE POLICY definidas en una tabla y aun así estar expuesta
públicamente si falta `ALTER TABLE x ENABLE ROW LEVEL SECURITY`. Supabase no bloquea
la tabla hasta que ese ALTER se ejecuta, independientemente de las políticas.

Fix: en cada migración que crea una tabla, ambas líneas obligatorias juntas:
  ALTER TABLE x ENABLE ROW LEVEL SECURITY;
  CREATE POLICY ...

Tablas solo accedidas por service_role (admin): también necesitan el ENABLE,
pero no necesitan políticas (service_role bypasa RLS igualmente).

Supabase envía alerta de seguridad con 24-48h de retraso — no confiar en que
avise en tiempo real. Verificar en Authentication > Policies tras cada migración.

Diagnóstico: comparar CREATE TABLE vs ENABLE ROW LEVEL SECURITY en migrations.
Cualquier tabla en el primero que no aparezca en el segundo está expuesta.
