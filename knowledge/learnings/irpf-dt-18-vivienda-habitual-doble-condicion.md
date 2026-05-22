---
name: irpf-dt-18-vivienda-habitual-doble-condicion
description: Deducción vivienda habitual DT 18ª LIRPF exige DOS condiciones acumulativas — pre-2013 + rdto previo < 33.007,20€.
date: 2026-05-22
source: claude-code-session
tags: [irpf, modelo-130, fiscal, deducciones]
---

**Bug crítico**: la deducción por vivienda habitual del modelo 130 (casilla 16) requiere **AMBAS** condiciones, no solo la primera:

1. Adquisición vivienda **pre-2013** (Disp. Trans. 18ª LIRPF tras supresión 2013)
2. **Rendimiento neto del ejercicio anterior < 33.007,20€/año**

Implementación común errada: solo comprueba (a) → cliente con hipoteca pre-2013 y rdto previo alto (ej. 35.000€) se autoaplica deducción 2% sobre c03 (máx 660,14€/trim) **NO permitida** → sanción LGT art 191 (50-100% cuota).

**Constante umbral en céntimos**: `UMBRAL_RENDIMIENTO_VIVIENDA_X100 = 3_300_720`.

**Fix**: guard en helper `calcularDeduccionViviendaHabitual()`:
```
if (rendimiento_neto_ejercicio_anterior_x100 >= 3_300_720) return 0n
```

**Caso 130 ejercicio 2026** verificado verbatim AEAT instrucciones. Aplica a cualquier calculador IRPF España que implemente DT 18ª.
