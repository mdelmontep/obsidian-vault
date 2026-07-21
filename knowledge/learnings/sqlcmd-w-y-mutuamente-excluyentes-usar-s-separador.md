---
title: sqlcmd -W y -y/-Y son mutuamente excluyentes, usar -s para separador real
date: 2026-07-21
source: claude-code-session
tags: [sql-server, sqlcmd, docker, etl]
---
Al extraer datos de SQL Server vía `sqlcmd -h-1` para volcar a PSV: `-W` (trim de padding) y `-y N`/`-y0` (ancho de columna) son **mutuamente excluyentes** — combinarlos falla con "The -W and the -y/-Y options are mutually exclusive". Post-procesar la salida de `-W` con `sed`/`awk` colapsando espacios rompe columnas de texto con espacios internos (nombres, direcciones).

Fix: usar `-W -s"|"` (separador de columna explícito de sqlcmd) — da un PSV real sin depender de colapsar espacios. Sin `-s`, columnas largas quedan con padding a la derecha; trim en destino.

Bonus gotcha del mismo dump: SQL Server puede devolver NUL bytes / mojibake windows-1252 en texto (nombres con `\x00\x00` al final) que rompen el body JSON de `supabase-js` ("unsupported Unicode escape sequence") — sanear siempre con `.replace(/[\x00-\x1f]/g, '')` tras `.trim()` antes de insertar.
