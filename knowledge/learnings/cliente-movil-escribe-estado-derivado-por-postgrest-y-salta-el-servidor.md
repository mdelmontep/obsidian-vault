---
title: un cliente móvil que escribe por postgrest se salta el escritor único del estado derivado
date: 2026-10-04
source: facturaia #3233 / #3242, tufacturaia-ios#32
tags: [supabase, postgrest, rls, triggers, ios]
---
**Qué pasa:** el estado de cobro (`facturas.estado`) se deriva del ledger de pagos y lo escribe una sola función. La web lo respetaba, pero la app iOS hacía `update {estado:'pagada'}` por PostgREST con la sesión del usuario. RLS lo dejaba pasar, porque la fila era suya. Resultado: facturas pagadas sin ningún pago detrás, y el cashflow, que cuenta pagos reales, las daba por 0 €.

**Por qué no se vio:** al auditar «quién escribe X» se hizo grep del repo web. El cliente móvil vive en otro repo y habla directamente con la base.

**Patrón:**
- Ante un dato derivado incoherente en prod, buscar escritores también en los repos de los clientes nativos (iOS, Android, scripts), no solo en el servidor.
- Candado en la base, no en el código: un trigger `BEFORE UPDATE OF <col>` que solo frene a `current_user = 'authenticated'` (service_role y las funciones SECURITY DEFINER pasan) y que exija la invariante, por ejemplo «pagada ⇒ hay pagos vivos», con ERRCODE propio.
- La migración incluye el backfill de las filas ya rotas y una autoverificación con un criterio independiente.
- El candado rompe la versión publicada del cliente hasta que salga la nueva: decidirlo y avisar.
