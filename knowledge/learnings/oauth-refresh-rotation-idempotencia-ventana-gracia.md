---
title: rotación de refresh: ventana de gracia para no revocar reintentos legítimos
date: 2026-06-20
source: claude-code-session
tags: [oauth, mcp, seguridad, facturaia]
---
La rotación de refresh con detección de reúso (token ya `rotated_to` → revoca la familia) tiene un falso positivo: un **reintento legítimo** (respuesta del `/token` perdida por red, doble submit, dos pestañas) reenvía el MISMO refresh ya rotado → se interpreta como robo → revoca familia → **logout del usuario legítimo**.

No es trivialmente idempotente: solo se guarda `sha256(token)`, nunca el plano → en el reintento NO puedes re-devolver el mismo token nuevo.

Fix (RFC 9700 §4.14.2) — **ventana de gracia**: si el hijo de la rotación se creó hace `<= N s` (default 15) y lo presenta el MISMO `client_id` → reintento benigno: emite un par nuevo en la familia SIN revocar. Fuera de la ventana, o de otro cliente → reúso → revoca. La carrera de `markRotated` pasa de revocar a benigna. Sin migración: la antigüedad se deriva del `created_at` del hijo. `grace=0` restaura el estricto.

Tradeoff: durante la ventana coexiste >1 refresh válido en la familia (overlap acotado). La alternativa (caché de la respuesta en claro) rompe la propiedad hash-only. TuFacturaIA #061 (PR #432). Ver [[signOut-solo-invalida-refresh-no-access-token]] · [[mcp-scope-grantable-vs-verifier-divergen]].
