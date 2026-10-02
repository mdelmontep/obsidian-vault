---
title: la vista previa de un lote calculada en la ui promete lo que el servidor salta
date: 2026-10-02
source: agh-iberica #2184 (revisión del contrato, RRHH #1702)
tags: [ui, hitl, contratos-de-api, testing]
---
- **Qué pasó:** «Aprobar los 6 comprobados» marcaba «Se aprobará» en NIF y en campos dudosos. El servidor (`apply-decisions.ts`) los salta en el lote: solo `verified` + `new`, sin NIF, y la fecha de efecto solo si su salario va dentro. Se guardaban 4, y la UI enseñaba 6.
- **Por qué no lo vio nadie:** los tests de la UI y los del servidor estaban en verde por separado. Cada lado tenía su propia regla y ningún test las cruzaba. Solo salió al guardar de punta a punta y contar las filas.
- **Gemelo:** guardar con algunos campos sin decidir dejaba el documento en `proposed`, y la API no devuelve lo ya decidido. Al reabrir, todo volvía a salir pendiente.
- **Fix:** una función de UI que replica la regla del servidor cláusula a cláusula (`hrClavesDelBloque`), con un test por cada cláusula. Además, Guardar exige que todo esté decidido.
- **Patrón:** toda acción en lote, previsualización o recuento («se aplicarán N») que calcula el cliente es una segunda copia de la regla del servidor. O la devuelve el servidor (dry-run), o se prueba contra él. Un E2E que cuenta las filas escritas es lo que la caza.
