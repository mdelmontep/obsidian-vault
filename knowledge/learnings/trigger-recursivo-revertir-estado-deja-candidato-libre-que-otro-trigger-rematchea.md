---
title: Trigger recursivo cuando revertir estado deja "candidato libre" que otro trigger re-matchea
date: 2026-05-20
source: facturaia mig 112 → 114 (F4 detect_reembolso)
tags: [postgres, triggers, recursion, conciliacion, stack-overflow]
---

# Síntoma

`stack depth limit exceeded` al INSERTar movimiento bancario negativo que dispara F4 detect_reembolso.

# Cadena

1. INSERT mov -100€ → AFTER INSERT `auto_mark_pagadas_on_movimiento` → llama `detect_reembolso_movimiento`.
2. detect_reembolso encuentra mov +100€ original conciliado a factura cobrada → UPDATE factura SET `estado='pendiente'`, `cobrada_con_movimiento_id=NULL`, `fecha_cobro=NULL`.
3. trg_auto_cobrada_on_factura (mig 103) fire → busca cobro libre. El +100€ original ya NO está reclamado (paso 2 lo liberó) → re-matchea → UPDATE factura SET `estado='cobrada'`, `cobrada_con_movimiento_id=v_mov_id`.
4. trg_mirror_factura_match_to_nn → INSERT mfa.
5. trg_zzz_mfa_recompute → recompute_factura_estado → UPDATE factura.
6. Vuelve a paso 3 → loop infinito.

# Causa raíz

Revertir el estado fiscal **no es suficiente** si el candidato (mov +100€) sigue visible para el trigger competidor que lo re-matchea inmediatamente. La señal "esto fue devuelto, no auto-conciliar" debe estar **en el candidato**, no solo en la factura.

# Solución (no solo `pg_trigger_depth`)

1. **Marca el candidato como neutralizado primero**: INSERT/UPSERT en `movimiento_metadata` con `devolucion_de_movimiento_id = <mov_original_id>` **ANTES** del UPDATE en facturas.
2. **Predicado de exclusión en el trigger competidor**: 
   ```sql
   AND NOT EXISTS (
     SELECT 1 FROM movimiento_metadata mm2
     WHERE mm2.devolucion_de_movimiento_id = mb.id
   )
   ```
3. Guard `pg_trigger_depth() > N` solo como defensa (cura síntoma, no causa).

# Lección general

Cuando dos triggers compiten por "mantener consistencia" en direcciones opuestas (uno marca cobrada, otro desmarca), revertir solo el estado deja al primero re-disparar inmediatamente. La separación de concerns exige que el segundo trigger **marque también la causa de la reversión** en forma que el primero pueda leer y excluir.

Aplicable a: workflows de aprobación con cancel, locks optimistas, sync bidireccional cross-tabla.

Relacionado: [[campo-sincronizado-entre-tablas-debe-poblarse-en-todos-los-puntos-de-escritura]]
