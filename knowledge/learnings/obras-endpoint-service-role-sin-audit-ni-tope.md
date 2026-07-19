---
title: endpoint que muta con service_role pierde auditoría; agregado histórico sin tope escanea todo
date: 2026-07-19
source: claude-code-session
tags: [facturaia, obras, auditoria, rendimiento, supabase]
---

Patrón recurrente detectado en 3+ cierres del módulo Obras de FacturaIA (aplica a cualquier proyecto Supabase con trigger de audit por RLS):

1. **Escritura con `createAdminClient` (service_role) → sin rastro.** El trigger de auditoría (en FacturaIA la mig `049`) solo dispara cuando `auth.uid()` no es null. Toda mutación server-side con service_role lo bypasa → PII y cambios mueren sin traza. Fix: `logAgentAction({ actor: 'human', orgId, userId, accion, entidad, entidadId, detalles })` explícito. En PII no vuelques el valor nuevo (teléfono/email) al detalle: registra qué campos cambiaron; en DELETE captura antes lo que identifica la fila.

2. **Agregado por periodo sin tope de ventana → escaneo del histórico completo.** Un endpoint de informes que acepta `desde/hasta` sin cota deja pasar `1900-2100` y fuerza un scan agregado sobre todas las facturas/pedidos. Fix: acotar en el único choke point de validación (máx N años).

Ambos son fallos silenciosos: no rompen build ni tests, solo se ven en producción (auditoría vacía / query lenta). Regla preventiva en `docs/architecture/gotchas.md §Obras`.
