---
name: github-actions-org-private-free-tier-2000-min
description: GitHub Actions org privadas — 2000 min/mes gratis, agotarlos dispara error de "payments have failed" sin haber intentado cobrar nada
date: 2026-05-21
source: claude-code-session
tags: [github, ci, billing, gotcha]
metadata:
  type: feedback
---

GitHub Actions da **2000 minutos/mes gratis** para repos privados de organizaciones. Cuando se agotan + spending limit en $0 (default), GitHub rechaza jobs futuros con:

> "recent account payments have failed or your spending limit needs to be increased"

El copy es **misleading**: dice "payments have failed" aunque NUNCA se haya configurado tarjeta. En realidad solo se agotó el cupo gratis. Caso real: org `AgentesIA-MAdrid` 2026-05-21, Manu nunca metió tarjeta.

**3 opciones para desbloquear**:
1. Esperar reset día 1 mes siguiente (gratis).
2. Hacer el repo público (minutos ilimitados, pero expone código).
3. Configurar tarjeta + subir spending limit (ej. 10$/mes; suele costar 0€ real).

**Verificar cuál es el caso**: org Settings → Billing → "Actions & Packages" muestra `X / 2000 min` consumidos. Si "Payment information" dice "No payment method on file" → es agotamiento de cupo puro, no caducidad de tarjeta.

**Reducir consumo (no agotar el cupo)**: en repo privado, CI con `push:[main]` + `pull_request` corre **2× cada commit** (el PR ya valida con branch protection; el push tras el merge es el mismo commit) → dejar solo `pull_request`. Añadir `concurrency: { group: ..., cancel-in-progress: true }` para matar runs superados. Caso `facturaia` #367 (2026-06-17): ~½ minutos y ½ emails de fallo.

Relacionado: [[dokploy-webhook-independiente-del-ci-status]] — el despliegue sigue funcionando aunque Actions esté bloqueado.
