---
title: cada aviso una sola superficie — el panel de avisos solo contiene accionables
date: 2026-06-10
source: claude-code-session
tags: [ux, frontend, avisos, design]
---
Si la misma información vive en badge de cabecera + banner + panel de avisos, el usuario percibe "demasiado aviso" y deja de leer todos — incluidos los críticos. Feedback literal: "demasiada información... demasiado aviso... que sea más guía".

Regla:
- Cada pieza de información vive en UNA superficie.
- Lo informativo permanente (periodicidad, feature pendiente) → badge o banner único.
- El panel de avisos/cuadres → SOLO accionables (algo que el usuario puede corregir ahora).
- Estado vacío → guía (qué es esto, cuándo aplica, CTA), no acumulación de warnings.

Implementación barata: `Set` de tipos redundantes filtrado antes de render (`cuadres.filter(c => !REDUNDANTES.has(c.tipo))`), sin tocar el backend.

Caso real (TuFacturaIA 349, PR #177): periodicidad y export-pendiente vivían en badge+banner Y en el panel → filtrados; panel quedó solo con falta-nif-iva/falta-clave/registro-negativo.
