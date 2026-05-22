---
name: aib-intracom-excluido-regimen-anticipos-liva-75-dos
description: LIVA art 75.Dos excluye AIB intracom (Uno.6º) y EIB (Uno.8º) del régimen de anticipos. Fecha cobro_anticipo NO aplica.
date: 2026-05-22
source: claude-code-session
tags: [aeat, iva, intracom, devengo]
---

**Gotcha**: LIVA art 75.Dos dice "Lo dispuesto en el apartado anterior [anticipos: devengo al cobro] **no será aplicable** a las entregas comprendidas en el número 6º (AIB) ni en el 8º (EIB) del apartado Uno". Aplicar `fecha_cobro_anticipo` a AIB intracom recibido = **bug fiscal**.

**Regla correcta AIB intracom recibido**: `fecha_devengo = min(fecha_factura, día_15_mes_siguiente_a_operacion)` (LIVA art 75.Uno.6º).

**Orden de evaluación en helper `fechaDevengoIva`**:
1. Criterio caja → throw (régimen no soportado MVP)
2. **AIB intracom recibido → regla AIB (NO mirar es_anticipo)**
3. Anticipo (resto de casos)
4. Tracto sucesivo
5. General: COALESCE(fecha_operacion, fecha)

**Ejemplo bug**: factura AIB DE recibida 20-feb-2026, fecha_operacion 5-feb, cliente registra fecha_cobro_anticipo 15-ene:
- Bug: devengo = 15-ene-2026 (T1 incorrecto)
- Correcto: devengo = min(20-feb, 15-mar) = 20-feb (T1, periodo correcto)

Aplica a cualquier calculador IVA con operaciones intracomunitarias.
