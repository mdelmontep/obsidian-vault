---
title: un pattern más estrecho que el dato del cliente bloquea el alta antes de escribir código
date: 2026-08-30
source: facturaia
tags: [migracion, validacion, config, onboarding]
---
El plan de cuentas de AGH usa códigos de **11 dígitos**. `src/lib/modules/catalog.ts:314-321`
valida los ocho `pgc_cuenta_*` con `^[0-9]{3,4}$` (clientes/proveedores base) y `^[0-9]{3,8}$`
(las otras seis). La configuración por organización existía y era correcta; lo que no admitía
al cliente era el **pattern**, no el modelo.

Al planificar la entrada de un cliente con datos propios (plan contable, series, códigos de
producto, NIF extranjeros), **medir sus datos reales contra los CHECK y los `pattern` de
config existentes antes de diseñar nada**. Es un `grep` de diez minutos que reordena el plan:
aquí convirtió «relajar un regex» en el paso 0 de la fase 2, y sin él el alta habría fallado
en validación con todo el backend ya escrito.

Relajar un `pattern` a un rango mayor es cambio seguro: ninguna config que validaba deja de
validar. Estrecharlo no. → [[facturaia-yooz-agh-migracion]]
