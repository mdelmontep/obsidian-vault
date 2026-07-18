---
title: cifrado a nivel columna se despliega en fases; el dual-write degrada, no falla
date: 2026-07-18
source: FacturaIA — auditoría cifrado, A6 (cifrar IBAN)
tags: [cifrado, migraciones, rollout, rgpd, facturaia]
---

# Migrar una columna a cifrado sin romper prod = fases + dual-write tolerante

Cifrar una columna existente (IBAN, cuenta) NO es un solo cambio. Fases no destructivas:
1. **DDL aditiva**: añadir `col_enc`/`col_bidx` (mig), sin tocar la plaintext.
2. **Dual-write**: los writers escriben plaintext + enc/bidx. Los **lectores siguen en plaintext** (sigue poblado) — no se toca lectura aún.
3. **Backfill** de datos históricos (job por lotes, la clave no está en BD → desde app).
4. **Cutover**: lectores → `readCol` (enc con fallback), luego DROP plaintext. Aquí el cifrado pasa a fail-closed.

**Gotcha clave del dual-write**: si el cifrado lanza (env de clave ausente en el deploy, valor no normalizable), NO debe romper el flujo (importación, alta de cliente) — el plaintext sigue siendo la verdad y el backfill re-poblará. El helper **degrada a plaintext-only + log alto**, no fail-closed. El fail-closed se activa en el cutover. Un deploy antes de setear las envs no debe tumbar nada. Ver [[blind-index-scoped-por-tenant]].
