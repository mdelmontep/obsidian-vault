---
title: migrations por módulo si commits van por módulo
date: 2026-05-11
source: claude-code-session
tags: [migrations, git, supabase]
---

Si N commits cubren N módulos independientes (OCR, Conciliación, Copiloto…), las migrations deben ir en **N archivos separados** numerados consecutivamente, no en un monolítico.

**Anti-patrón**: `060_module_triggers.sql` con triggers de 3 módulos distintos → un commit "feat OCR" arrastra cambios de Conciliación y Copiloto, ilegible en `git log`.

**Patrón correcto**:
- `060_ocr_auto_categorizar_trigger.sql` ← commit OCR
- `061_conciliacion_auto_marcar_pagada.sql` ← commit Conciliación
- `062_copiloto_conversaciones.sql` ← commit Copiloto

**Ventajas**:
- Rollback granular: una migration mala se revierte sin tocar las otras
- Diff legible: cada commit incluye solo SU migration
- Atribución limpia: `git blame` apunta al commit del módulo correcto
- Aplica orden: si una falla a mitad, Supabase deja claro en cuál se paró

**Caso real FacturaIA**: arranqué con `060_module_triggers.sql` todo junto, lo reseparé en 060+061 antes de commitear porque iba a hacer 4 commits per-módulo. Hubiera sido caótico.

**Coste**: marginal — separar archivos es 30 segundos. Mucho menos que el coste futuro de un rollback parcial mal hecho.
