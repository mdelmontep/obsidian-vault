---
title: FacturaIA auditoría cifrado — prompt de continuación
date: 2026-07-18
source: claude-code-session
tags: [facturaia, seguridad, cifrado, continuacion]
---

Estado y handoff de la auditoría de cifrado. Hub: [[facturaia]] §Seguridad. PR #998 (`feat/seguridad-cifrado`).

## Hecho y en PR #998 (gates verdes, Fable 5 por bloque; migs validadas en Supabase local)
- Fase 1: A1 `src/lib/crypto/pii.ts` (AES-256-GCM kid + blind index HMAC scoped por org), A4 cifrado .p12 VeriFactu + IV 12B, A8 cache-control PDFs, A9 fix doc §OTP, A10 kid+runbook webhooks/signing, B5-f1 warning clave no-64-hex.
- Fase 2: A5 **mig 513** (columnas `*_enc`/`*_bidx`/`cuenta_mask` + `cuentas_bidx`), A6 dual-WRITE IBAN/cuenta (movimientos-insert, 2 sync PSD2, clientes/proveedores crear-rapido, mandatos, ocr-process; degrada a plaintext-only si faltan envs; lectores en plaintext), A3 **mig 514** (phone_change_revoke_tokens→token_hash vía trigger + reescritura fiel de change_phone_revoke), A2 **mig 515** (fiscal_share_tokens → id uuid PK + token_hash + token_suffix; enlaces show-once, revoke por id).
- Decisiones: B4 ADR-010 ACEPTADO (env+hardening+kid, no Vault). B6 mantener TTL 7d.
- Validado con `supabase start` local: las 486 migraciones (incl. 513/514/515) aplican; `gen types --local` = mis 9 columnas. Ver [[validar-migracion-en-supabase-local-sin-tocar-prod]] · [[supabase-start-colima-macos-vector-container-falla]].

## Precondiciones de despliegue (antes de mergear PR #998)
1. Envs Dokploy: `PII_BANK_ENCRYPTION_KEY` + `PII_BANK_INDEX_KEY` (64-hex, DISTINTAS).
2. Aplicar migs 513-515: `supabase db push --linked` desde main limpio + `gen:types` (verificar antes `migration list --linked`; el MCP apunta a PROD, no usar).
3. Smoke E2E: A6 (IBAN → *_enc/*_bidx), A2 (enlace crear/abrir/revocar por id), A3 (cambio tel→confirm→email revoke→click→swap-back).

## Pendiente — ORDEN DE DESPLIEGUE ESTRICTO: deploy Fase1+2 → B1 (prod) → A7 → B2
- **B1** backfill datos reales (acción Manuel; script idempotente por lotes, cifra desde app): clientes.iban, proveedores.iban, sepa_mandatos.iban/bic, movimientos_bancarios.cuenta, conciliacion_reglas.cuentas→cuentas_bidx. (fiscal/phone ya se backfillean en 514/515.)
- **A7** matching por blind index, SOLO tras B1 (si no, rompe matching histórico sin bidx): transfer-pairs.ts, transferencia-candidatas.ts, antifraud/bank-anomaly.ts (R1/R4)→cuenta_bidx; migración reescribe función de 271 a `cuenta_bidx = ANY(cuentas_bidx)`; trigger 368 compara iban_bidx; UI reglas muestra cuenta_mask. Desarrollable ya contra local, NO mergear hasta B1-en-prod.
- **B2** cutover destructivo (tras B1): lectores→readIban/readCuenta (helper en iban-fields.ts); DROP columnas plaintext (iban/cuenta/bic/token); reescribir RPCs merge 245/259/467; retirar degradación de iban-fields; excluir *_enc de selects al navegador. Precondición P1: mover write de IBAN de `clientes-view.tsx` (navegador) a endpoint servidor, o re-backfill+freeze.

## Entorno local (worktree)
`supabase/config.toml` UNTRACKED (no commitear): puertos +30 + `[analytics] enabled=false`. Retomar: `colima start && supabase start`; parar: `supabase stop`. Puertos Postgres remotos bloqueados en esta red → usar local.

## Al retomar
1. `git fetch && git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d` (re-verificar colisión 513-515; si main avanzó, renumerar + re-merge origin/main).
2. Decidir con Manuel: ¿corrió B1 en prod? Sí→mergear A7; No→desarrollar A7 contra local.
