---
title: pgcrypto en supabase cloud está en schema extensions, no public
date: 2026-04-27
source: claude-code-session
tags: [supabase, postgresql, triggers, pgcrypto]
---

## Problema
Triggers con `SET search_path = public` no encuentran `digest()` aunque pgcrypto esté activado.
El error es: `function digest(text, unknown) does not exist`

## Causa
En Supabase Cloud, pgcrypto se instala en el schema `extensions`, no en `public`.

## Fix
```sql
CREATE OR REPLACE FUNCTION mi_trigger()
...
SET search_path = public, extensions  -- añadir extensions
AS $$
  ...
  NEW.campo := encode(extensions.digest(input, 'sha256'), 'hex');  -- cualificar
$$;
```

Llamar `extensions.digest()` explícitamente además de añadirlo al search_path.
