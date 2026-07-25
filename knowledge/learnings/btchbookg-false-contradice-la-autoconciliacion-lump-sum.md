---
title: BtchBookg false contradice la auto-conciliación lump-sum
date: 2026-07-25
source: claude-code-session
tags: [sepa, pain008, conciliacion, facturaia]
---

`BtchBookg` en el `PmtInf` de pain.008 decide cómo apunta **tu** banco la remesa en **tu** extracto. No afecta al deudor, que ve su cargo igual.

- `false` → un apunte por cada adeudo.
- `true` → un único apunte agregado por remesa.

FacturaIA lo tenía fijo en `false` (`pain008.ts:159`) mientras su auto-conciliación (`findUniqueMovimiento`, `conciliacion-remesa.ts`) busca **un** movimiento cuyo importe sea exactamente `ctrl_sum`. O sea, le pedíamos al banco justo lo contrario de lo que necesitábamos para casar.

Remesa de 40 cuotas de 45 € = 1.800 €:
- con `true`, existe el apunte de 1.800 €, casa único y exacto, y las 40 facturas se marcan cobradas solas;
- con `false`, hay 40 apuntes de 45 € y ninguno de 1.800. `findUniqueMovimiento` devuelve `null`. Y aunque se intentase casar línea a línea, 40 importes idénticos son ambiguos entre sí, así que el filtro `matches.length === 1` también daría `null`.

**Matiz:** muchas entidades españolas ignoran la etiqueta y aplican lo pactado en el contrato de adeudos. Es "pedirlo bien", no garantizarlo.

**Riesgo al cambiarlo:** se pierde el desglose por factura en el extracto (irrelevante para la app, que reparte vía `asignar_manual`, pero no para una gestoría que cuadre a mano), y si el banco netea las devoluciones antes de apuntar el total, el agregado deja de coincidir con `ctrl_sum` y la conciliación falla igual.

Regla general: **cuando el sistema pide algo a un tercero y otra parte del sistema asume la respuesta contraria, uno de los dos está mal.** Merece la pena revisar cada constante hardcodeada de un protocolo contra lo que el propio código espera recibir.

Ver [[facturaia-modulo-sepa-config]].
