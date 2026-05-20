---
title: Guard per-transición no persiste si otro trigger re-UPDATEa con OLD distinto
date: 2026-05-20
source: facturaia mig 117 → 128 (guard revert reembolso)
tags: [postgres, triggers, guard, recompute-chain]
---

# Síntoma

Guard `IF OLD.estado='cobrada' AND NEW.estado='pendiente' THEN RETURN NEW` no impide que el trigger re-cobre la factura tras una devolución. Visible en `module_events`: 2 eventos `factura_cobrada_auto` al mismo timestamp + N:N con fila desvinculada por mirror + fila nueva creada al instante.

# Causa

El chain `mirror_factura_match_to_nn → trg_zzz_mfa_recompute → recompute_factura_estado` UPDATEa la factura **otra vez** con `OLD.estado='pendiente'`. El mismo trigger fire pero `OLD.estado` ya no es `'cobrada'` → guard no aplica → SELECT encuentra candidato libre → re-cobra.

# Fix

Sustituir guard transition por **persistente** vía columna timestamp:
- `detect_*` setea `last_revert_at = NOW()` en el UPDATE de revert.
- Trigger competidor filtra `AND (last_revert_at IS NULL OR last_revert_at < NOW() - INTERVAL '30 days')`.
- Ventana 30d permite re-asignación tras tiempo razonable. Manual via UI bypassa (escribe directo cobrada_con_movimiento_id, no pasa por trigger de auto-match).

# Lección general

Guards sobre `OLD.X` asumen que el siguiente UPDATE viene del mismo punto. Si hay chain de triggers que re-UPDATEan, `OLD.X` cambia y el guard falla silenciosamente. Para protección persistente: columna explícita + filtro temporal o booleano que sobreviva al chain entero.

Relacionado: [[trigger-recursivo-revertir-estado-deja-candidato-libre-que-otro-trigger-rematchea]]
