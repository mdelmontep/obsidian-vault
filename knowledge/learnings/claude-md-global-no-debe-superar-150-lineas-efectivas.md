---
title: claude-md global no debe superar 150 lineas efectivas
date: 2026-04-21
source: claude-code-session
tags: [claude-code, optimizacion, buenas-practicas]
---

Con más de ~150 líneas en CLAUDE.md, la densidad de instrucciones degrada — Claude empieza a ignorar reglas del final del archivo. El presupuesto efectivo de instrucciones es ~100-150 (el sistema base ya consume ~50).

Síntomas de un CLAUDE.md demasiado grande:
- Reglas al final del archivo se incumplen con más frecuencia
- Gotchas específicos de un tema (n8n, Retell, Supabase) se cargan aunque la sesión no toque ese tema
- Tokens desperdiciados en cada mensaje sin beneficio

Solución aplicada:
- Reglas genéricas → CLAUDE.md global
- Gotchas por tema → vault `Stack/` (carga bajo demanda)
- Gotchas por proyecto → `<repo>/CLAUDE.md` (carga solo en ese repo)
- Credenciales/referencias → memory files (consulta puntual)

Para cada línea del CLAUDE.md, preguntar: "si quito esto, ¿Claude cometerá errores?" Si no → no pertenece ahí.
