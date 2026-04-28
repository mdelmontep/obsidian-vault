---
title: postgres template tokens con replace simple no rechaza tokens desconocidos
date: 2026-04-28
source: claude-code-session
tags: [postgres, plpgsql, validation]
---

Función PL/pgSQL que sustituye tokens (`{CODIGO}`, `{AAAA}`, `{NNNN}`...) con `replace()` en cadena deja **literal** lo que no reconoce. Si el usuario escribe `{PAPA}` por error, se guarda en BD `{PAPA}{AAAAMM}-1231` y aparece como número de factura.

## Patrón: tres redes

1. **CHECK constraint en BD** con función `is_valid_<thing>(text)` que extrae todos los `{...}` por regex y exige que cada uno esté en allowlist + que haya al menos un token contador. Defensa en profundidad cuando UI/API fallan.
2. **Validación en API** (POST y PATCH) con la misma allowlist en TS, error 422 si inválido.
3. **UI** con la misma función, deshabilita Guardar y muestra el token concreto que falla.

Mantener las tres listas sincronizadas — allowlist en SQL, TS y picker UI. Si añades token nuevo, los 3 sitios.

Mig 021 de FacturaIA: `is_valid_series_format` + `ALTER TABLE ... ADD CONSTRAINT ... CHECK`.
