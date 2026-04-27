---
title: triggers postgres para auditoría automática por tabla
date: 2026-04-27
source: claude-code-session
tags: [postgres, supabase, auditoria, triggers]
---

- Trigger `AFTER INSERT OR UPDATE OR DELETE FOR EACH ROW` en tablas principales
- Resolver actor: `auth.uid()` → human. Si null → saltar (agentes loguean directo con insert)
- Campos auditables por tabla en array — comparar OLD vs NEW solo en esos campos
- Si diff vacío en UPDATE → `RETURN NULL` sin insertar (evita ruido de `documento_url`, `updated_at`)
- Fallo silencioso: `EXCEPTION WHEN OTHERS THEN NULL` — log nunca bloquea la operación
- Detección correcciones IA: lookup en `bandeja_ingesta WHERE factura_id = NEW.id AND fuente IN ('email','whatsapp','voz')` — excluir `'manual'`
- Agentes (service_role, sin `auth.uid()`) loguean directamente en `audit_log` desde la API route con `actor_type` explícito
- `SET LOCAL app.actor` no funciona entre queries SDK — no hay transacción implícita entre llamadas PostgREST
