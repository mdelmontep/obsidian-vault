---
name: verifactu-aplazado-2027-rdl-15-2025
description: Verifactu (RD 1007/2023) APLAZADO a 2027 por RDL 15/2025. Durante 2026 voluntario. IS 01-ene-2027, IRPF/IRNR-EP 01-jul-2027.
date: 2026-05-22
source: claude-code-session
tags: [verifactu, aeat, fiscal, calendario]
---

**Cambio normativo crítico**: el Real Decreto-ley 15/2025 (BOE 03-dic-2025) APLAZÓ la obligación de Verifactu:

- **Impuesto Sociedades**: obligatorio desde 01-ene-2027
- **IRPF / IRNR-EP** (autónomos persona física + establecimientos permanentes): obligatorio desde 01-jul-2027
- **Durante 2026**: completamente voluntario — un autónomo o PYME puede emitir facturas sin Verifactu en 2026 sin sanción

**Gotcha**: la spec inicial del módulo asumía obligación 2026. Cualquier cuadre/UI/marketing que diga "Verifactu obligatorio" en 2026 es bug.

**Lo que SIGUE válido**:
- Cuadres del estado actual `verifactu_estado='rechazada'` o `'error'` siguen detectando bugs reales (si lo activaron voluntariamente)
- Cuadre `'pendiente'` sigue válido como aviso (anticipa cumplimiento futuro)

**Lo que cambia**:
- NO asumir `verifactu_activo=true` por defecto en orgs 2026
- Mensaje UX claro: "Verifactu voluntario hasta 2027, obligatorio en {tu_caso}"
- Marketing puede vender "preparados para 2027" como ventaja anticipada

Aplica a cualquier dev fiscal España hasta julio 2027.
