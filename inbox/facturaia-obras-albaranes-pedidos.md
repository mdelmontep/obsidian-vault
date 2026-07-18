---
title: Obras — albaranes / pedidos / pedido→factura (mini-PRD futuro)
date: 2026-07-18
tags: [inbox, facturaia, obras]
---

Manuel quiere valorar/implementar más adelante que el módulo Obras genere también **albaranes, pedidos y la conversión pedido→factura** (y facturas de proveedor). Decidido diferir (18-jul), NO en la sesión de facturación.

Contexto/evidencia:
- Hoy `DocTipo` de TuFacturaIA = factura/factura_simplificada/abono/presupuesto/proforma. **No existe albarán ni pedido en toda la plataforma** (0 tablas, 0 migraciones).
- El PRD del módulo Obras los marca Out of Scope / Fase 2 (dependen de Logística/Almacén y Facturas de Proveedor, inexistentes).

Antes de implementar → mini-PRD con las decisiones fiscales:
- ¿El albarán es un documento NO fiscal que convierte a factura (como la certificación)? ¿Serie propia?
- ¿El "pedido" es de VENTA (cliente pide → convierte a factura) o de COMPRA (pedido a proveedor)? Son cosas distintas.
- Facturas de proveedor = lado de compras, arrastra el módulo de gasto/OCR de proveedor.

Relacionado: [[facturaia]] §Módulo Obras.
</content>
