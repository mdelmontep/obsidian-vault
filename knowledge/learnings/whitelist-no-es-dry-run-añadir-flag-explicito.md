---
title: Whitelist ≠ dry-run — añadir flag explícito si quieres seguridad en smokes
date: 2026-05-22
source: claude-code-session
tags: [testing, safety, dry-run]
---

Un guard "phone/email whitelist → permitido" no equivale a "dry-run". El sistema permite phones de test pero sigue ejecutando contra APIs reales (Clientify, Stripe, etc.). Resultado: smokes con phones de test crean registros reales que nadie limpia.

Heurística: si un humano puede dudar "¿esto crea registros reales?", añade flag explícito `dry_run:true` que cortocircuita el sub-workflow devolviendo IDs sintéticos (`wl-+<phone>`, `wl-deal-<ts>`). El flag se propaga en cascade por todos los sub-workflows downstream.

Bot real en producción NUNCA pasa `dry_run`. Smokes y agentes auditores SÍ lo pasan siempre.

Caso real Elphis 2026-05-22: smoke con `+34600000093` (whitelist) creó contact 161100276 + deal 29522631 reales en CRM con 1807 contactos. Tuve que borrar a mano. Diseñé dry_run quirúrgico en 4 sub-workflows.
