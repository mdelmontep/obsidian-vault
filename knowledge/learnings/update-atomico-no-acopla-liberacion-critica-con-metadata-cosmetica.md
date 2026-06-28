---
title: UPDATE atómico no debe acoplar liberación de recurso crítico con metadata cosmética
date: 2026-06-28
source: claude-code-session
tags: [postgres, crons, locks, watchdog, resiliencia, tufacturaia]
---

# UPDATE atómico: no acoplar lo crítico con lo cosmético

**Incidente TuFacturaIA 2026-06-28:** el watchdog de crons quedó en fallo permanente y arrastró al webhook-dispatcher (bloqueado >1h, webhooks sin enviar).

**Causa:** `cleanup_cron_zombies()` cerraba el lock (`finished_at`, CRÍTICO) y marcaba `status='zombie'` (COSMÉTICO) en el **mismo UPDATE**. `'zombie'` no estaba en el `CHECK` de la columna → `check_violation` tumbaba el UPDATE entero → el lock nunca se liberaba → el auto-curador se mató a sí mismo.

**Regla:** en una escritura atómica, separa **liberar el recurso** (solo campos sin constraint → no puede fallar) del **metadata informativo** (best-effort, en subbloque `BEGIN ... EXCEPTION WHEN check_violation THEN NULL`). Lo cosmético jamás debe poder tumbar lo crítico.

**Corolario (bug latente de constraint):** código que escribe un valor fuera del `CHECK` es invisible hasta que el path se ejercita por primera vez (aquí: el primer zombi que envejeció >20min en meses). Al añadir un estado en código → **grep el CHECK y amplíalo en la misma migración**.

Relacionado: [[alert-collector-cron-vs-live-dedup-gap]] · [[outbox-event-type-fuera-del-catalogo-muere-silencioso]]
