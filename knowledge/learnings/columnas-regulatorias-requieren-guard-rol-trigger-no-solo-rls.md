---
title: columnas regulatorias requieren guard de rol en trigger + API route, no solo RLS
date: 2026-05-19
source: claude-code-session
tags: [supabase, security, rls, audit, fiscal]
---

RLS basada en membership no protege columnas con efecto regulatorio (Verifactu, AEAT, GDPR, fiscal) si la policy de UPDATE no distingue rol. La policy típica `id = get_user_org_id()` permite a **cualquier miembro** (becario, comercial, contable) hacer UPDATE de la org desde DevTools del navegador, incluyendo apagar el envío a AEAT.

**Patrón canónico (defensa en profundidad):**
1. **Capa API**: Route Handler con `withApiAuth({ requireRole: ['propietario','admin'] }, ...)` + Zod + rate limit. Single entry point.
2. **Capa BD**: trigger BEFORE UPDATE que rechaza si `auth.uid()` tiene rol insuficiente. Cubre escapes: admin client mal usado, RPC futura, SQL directo, otra route que olvide el guard.
3. **Trazabilidad**: trigger AFTER UPDATE que escribe `audit_log` con `user_id`, IP/UA via `[[supabase-trigger-captura-ip-via-current-setting-request-headers]]`, old/new. Necesario para defensa regulatoria (AEAT exige trazabilidad).

**Trampa típica**: depender solo de RLS confiando en "el cliente solo expone el toggle a admins". Cualquier user autenticado puede saltarse la UI con `curl` + cookie de sesión.

Caso real: FacturaIA mig 095 (PR #48) — `verifactu_activo` + `entorno_verifactu`. Mismo patrón aplicable a `regimen_iva`, `nif`, `iae`, `verifactu_num_instalacion`.
