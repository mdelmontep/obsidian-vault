---
title: generar remesa sepa pain.008 (adeudo directo / cuaderno 19.14)
date: 2026-06-24
source: claude-code-session
tags: [sepa, banca, facturaia, xml]
---

- `SeqTp` (FRST/RCUR) va a nivel **PmtInf**, NO por operación → agrupar adeudos por tipo de secuencia en bloques `PmtInf` separados.
- Identificador de Acreedor ES: control = `98 - mod97(idNacional + "ES00")`, **excluyendo** el sufijo de 3 chars. Verificado: `ES35000B56876196` → 35.
- `DbtrAgt` = `NOTPROVIDED` si no hay BIC del deudor (válido SEPA por solo-IBAN).
- `CtrlSum` = suma en **céntimos enteros** (evita deriva float); debe cuadrar con `NbOfTxs`.
- Reutilizar el IBAN del acreedor (single source: ya estaba en `organizations.template_config.emisor.iban`) en vez de crear columna nueva.
- XML hand-rolled sin deps; **persistir el XML generado** (inmutable) para descarga reproducible y auditoría.
- Esquema CORE: el deudor particular puede devolver el recibo hasta 8 semanas → mantener `sepa_remesa_lineas` para conciliar devoluciones por `end_to_end_id`.
- **B2B**: misma estructura, única diferencia en XML = `LclInstrm/Cd` (CORE→B2B). Decisión bank-safe: una remesa = **un solo esquema** (NO ficheros mixtos CORE+B2B, muchos bancos los rechazan) → mig 389 amplía el CHECK; helper `esquemaUnico` rechaza mezcla. FacturaIA Fase A #490.
- RETORNO de devoluciones = pain.002.001.03 `CstmrPmtStsRpt` (`OrgnlEndToEndId` hijo de `TxInfAndSts`; `StsRsnInf/Rsn/Cd`), NO el pain.008 SALIENTE `CstmrDrctDbtInitn` (lo que exporta Holded, EndToEndId fijo). Verificar la raíz XML antes del parser. FacturaIA: #459 MVP; devoluciones Fase 1 en PR #470 (parser pain.002 + cruce E2E + revoca mandato muerto).
