---
title: facturaia auditoría — huecos restantes tras PR #685
date: 2026-07-04
source: claude-code-session
tags: [facturaia, auditoria, audit-log, seguridad, rama]
---

# TuFacturaIA — Huecos de auditoría restantes (post PR #685)

## Contexto

PR #685 (`fix/auditoria-atribucion-actor`, mergeado) arregló el bug reportado en un
screenshot de `Ajustes → Auditoría`: acciones del Copiloto aparecían como "Sin
identificar" y crear/emitir/anular factura desde la web se atribuía a "API" en vez
del usuario real. Detalle completo del PR y su smoke test → [[facturaia-historico-detallado]]
(buscar "auditoria-atribucion-actor" si hace falta el histórico exacto).

Tras cerrar ese PR, se pidió una pasada sistemática (3 agentes Explore en paralelo,
grep de `.insert(/.update(/.delete(/.upsert(` sobre Supabase en `src/app/api/**` y
libs relacionadas) para mapear **todos** los endpoints que mutan datos sin dejar
ningún rastro en `audit_log` (vía `logAgentAction()`, `src/lib/audit-agent.ts`) ni en
`admin_audit_log` (vía `logSystemAction()`, `src/lib/system/admin-audit.ts`).

Resultado: **~40 endpoints más con el mismo tipo de hueco**, muy por fuera del
alcance razonable de un solo PR. Este doc es el mapa completo + plan de ataque
troceado en PRs sucesivos.

**Regla transversal detectada**: muchos endpoints (sobre todo conciliación,
recurrentes, remesas) sí escriben en `module_events`/`product_events` y lo dan por
"auditado" — pero eso es un log de **analítica de producto**, no el sistema de
auditoría legal/seguridad que ve el usuario en `Ajustes → Auditoría`. No cuenta como
mitigación.

---

## Bloque 1 — Seguridad crítica (hacer primero)

| Endpoint | Qué hace | Por qué es crítico |
|---|---|---|
| `src/app/api/settings/security-policy/route.ts` PUT (línea ~98, `.upsert` sobre `org_security_policies`) | Activa/desactiva 2FA obligatorio, timeout de sesión, longitud mínima de contraseña para **toda la org** | Cambio de seguridad org-wide sin ningún rastro |
| `src/app/api/me/profile/route.ts` PATCH (línea ~68, `.update` sobre `profiles`) | Cambia `full_name` y **`phone`** directamente, sin pasar por el flujo OTP de `/auth/phone/*` | Vector de account takeover silencioso — el teléfono es la vía de recovery/WhatsApp |
| `src/app/api/clientes/[id]/merge/route.ts` (línea ~69, RPC `merge_cliente`) | Fusiona dos clientes: redirige facturas/presupuestos al target y **elimina** el cliente origen | Acción destructiva e irreversible sin rastro |
| `src/app/api/proveedores/[id]/merge/route.ts` (línea ~68, RPC `merge_proveedor`) | Mismo patrón, elimina proveedor origen | Idem |
| `src/app/api/auth/onboarding/fiscal/route.ts` POST (línea ~100, `.update` sobre `organizations`) | Fija **NIF y régimen de IVA** de la empresa | Dato fiscal/legal crítico; solo pasa por `logOnboardingEvent` (funnel/analítica), no por auditoría |
| `src/app/api/settings/password/route.ts`, `src/app/api/settings/sessions/route.ts` | Cambio de contraseña, revocar sesiones (`supabase.auth.updateUser`, `admin.auth.admin.signOut`) | Acciones de seguridad sin ningún log — no usan los 4 verbos SQL directos, pero son las más sensibles de toda la lista |

**Patrón de fix**: igual que en #685 — añadir `logAgentAction({ actor: 'human', orgId, userId, accion, entidad, entidadId, detalles })` tras la mutación, con `entidad` nueva si hace falta (`security_policy`, `profiles`/`telefono`, `clientes`/`proveedores` para merge). Para `merge_cliente`/`merge_proveedor`, registrar el `entidad_id` del origen (el que desaparece) antes de que el RPC lo borre.

---

## Bloque 2 — API pública v1 (patrón mecánico, igual al fix de #685)

Asimetría clara: los endpoints `facturas/*` de `v1` sí llaman a `logAgentAction` con
`actor: 'agent:api'`; sus hermanos de `clientes`/`proveedores`/`presupuestos`/`catalogo`
no.

| Endpoint | Verbo/tabla |
|---|---|
| `src/app/api/v1/clientes/route.ts` POST (vía `src/lib/clientes/crear-rapido.ts:169,208`) | insert/update `clientes` |
| `src/app/api/v1/clientes/[id]/route.ts` PATCH (línea ~97) | update `clientes` |
| `src/app/api/v1/proveedores/route.ts` POST (vía `src/lib/proveedores/crear-rapido.ts:174`) | insert `proveedores` |
| `src/app/api/v1/proveedores/[id]/route.ts` PATCH (línea ~112) | update `proveedores` |
| `src/app/api/v1/presupuestos/[id]/route.ts` DELETE (línea ~170, solo borradores) | delete `presupuestos` |
| `src/app/api/v1/presupuestos/[id]/marcar-aceptado/route.ts` (línea ~67) | update `presupuestos` |
| `src/app/api/v1/presupuestos/[id]/marcar-rechazado/route.ts` (línea ~57) | update `presupuestos` |
| `src/app/api/v1/catalogo/route.ts` POST (línea ~134) | insert `catalogo_servicios` |
| `src/app/api/v1/catalogo/[id]/route.ts` PATCH (línea ~104) | update `catalogo_servicios` |
| `src/app/api/v1/facturas/[id]/recordatorio-pago/route.ts` | envía email real al cliente; sus hermanos (`reenviar-email`) sí auditan, este no |
| `src/app/api/v1/stock/ajustes` POST | RPC `ajustar_stock_manual` — no verificable desde TS, revisar aparte |

Contraste útil: el tool de Copiloto `crearCliente.ts` sí llama a `logAgentAction`
tras usar la misma lib compartida (`crear-rapido.ts`) — el endpoint público v1 no.
Confirma que el hueco es real, no un false positive del grep.

**Patrón de fix**: añadir `logAgentAction({ actor: 'agent:api', orgId, userId (si viene de user-token), accion, entidad, entidadId, detalles: { api_key_id } })` en cada uno, mismo shape que `v1/facturas/route.ts` ya usa.

---

## Bloque 3 — Conciliación (el bloque más grande, merece diseño propio)

Casi todo el módulo usa `module_events` (analítica) en vez de `audit_log`. Antes de
tocar código, decidir: ¿ampliar `MODULE_EVENT_TO_AUDIT` en `src/lib/audit/feed.ts`
para que estos eventos ya existentes se re-usen en el feed de auditoría (barato, sin
tocar los endpoints), o añadir `logAgentAction` explícito en cada uno (más trabajo,
pero separa limpiamente analítica de auditoría)? Recomiendo lo primero como quick
win y lo segundo solo para las acciones más sensibles (editar/eliminar movimiento).

- **Reglas de conciliación** (CRUD completo, sin ninguna auditoría ni siquiera `module_events`):
  `src/app/api/conciliacion/reglas/route.ts` POST, `reglas/[id]/route.ts` PATCH/DELETE,
  `reglas-aprendidas/[id]/route.ts` DELETE, `reglas-aprendidas/route.ts` upsert.
- **Categorías contables**: `src/app/api/conciliacion/categorias/route.ts` POST (línea ~149).
- **Movimientos bancarios** (el corazón del módulo):
  - `movimientos/[id]/route.ts` — editar manualmente (línea ~387), soft-delete (línea ~578). Solo `module_events`.
  - `movimientos/bulk-revert`, `movimientos/bulk-confirm` — solo `module_events`.
  - `movimientos/[id]/registrar-ingreso/route.ts` — registrar/deshacer ingreso sin factura (incluye `motivo_no_sujeto`, dato fiscal). Solo `module_events`/`product_events`.
  - `movimientos/[id]/notas/**` — crear/editar/eliminar nota. Solo `product_events`.
  - `sugerencias/[id]/reject/route.ts` — rechazar match sugerido por IA. Sin nada.
- **Vía RPC, no verificable desde TS** (revisar si la función SQL audita algo):
  `movimientos/[id]/asignar`, `asignaciones/[id]/desvincular`, `anticipos/[id]/aplicar`,
  `movimientos/[id]/transferencia`, `movimientos/[id]/anticipo`, `movimientos/[id]/registrar-resto`,
  `facturas/[id]/registrar-resto`, `automarks/revertir`, `sugerencias/[id]/confirm`.

---

## Bloque 4 — Cobros, recurrentes, settings menores (baja prioridad)

- **Cobros**: `src/app/api/cobros/opt-out/route.ts` (+`revoke`), `src/app/api/cobros/send-now/route.ts`, y la lib `src/lib/cobros/orchestrator.ts` (líneas 223, 287, 306, 351) — dar de baja a un cliente de cobros, enviar recordatorio manual, transiciones de estado. Sin auditoría.
- **Facturas recurrentes**: `src/app/api/facturas-recurrentes/route.ts` POST, `[id]/route.ts` PATCH/DELETE, `revisiones/[id]/route.ts` DELETE, `src/lib/recurrentes/materializar.ts` (confirmar/emitir revisión). Solo `logModuleEventFireAndForget` en el mejor caso.
- **Remesas SEPA**: `src/app/api/sepa/remesas` y `remesas-pago` — mutan vía RPC (`crear_remesa_cobro`/`crear_remesa_pago`), solo `module_events`. No verificable desde TS.
- **Settings menores**: `email-config` PUT, `features` PATCH (activar/desactivar módulos, tiene lógica anti-bypass de pago pero el cambio en sí no se audita), `module-suggestions` PATCH, `whatsapp` PATCH, `profile/avatar` POST/DELETE (impacto bajo, cosmético).
- **Inventario**: `src/app/api/inventario/importar/route.ts` (sobreescritura masiva por Excel) + `src/lib/catalogo/create-producto.ts` (alta desde el mismo import).

---

## Decisión pendiente de diseño

Para conciliación en concreto: ¿el criterio es "todo lo que un humano hace debe
verse en `Ajustes → Auditoría`" (entonces hay que añadir `logAgentAction` en cada
endpoint, trabajo grande) o "basta con que quede en algún sitio auditable, aunque
sea `module_events`, y ampliamos el feed para leerlo de ahí" (quick win, cambia solo
`src/lib/audit/feed.ts`)? Esto determina si el Bloque 3 es 1 PR pequeño o 15+ PRs
mecánicos. Decidir con Manu antes de arrancar el Bloque 3.

---

## Prompt para arrancar la siguiente sesión

Copiar/pegar esto tal cual al empezar:

> Sigue con la auditoría de `audit_log` en TuFacturaIA. Contexto completo en
> `knowledge/projects/agentesia/facturaia-auditoria-huecos-restantes.md` (Obsidian).
> PR #685 ya cerró el bug original (Copiloto "Sin identificar" + atribución
> web→API). Lo que queda son ~40 endpoints más con el mismo tipo de hueco,
> troceados en 4 bloques por prioridad. Arranca por el **Bloque 1 (seguridad
> crítica)**: `settings/security-policy`, `me/profile` (cambio de teléfono sin
> OTP), `clientes/[id]/merge` y `proveedores/[id]/merge`, `auth/onboarding/fiscal`.
> Mismo patrón que #685: `logAgentAction({ actor: 'human', orgId, userId, accion,
> entidad, entidadId, detalles })` tras cada mutación, worktree propio, PR con
> smoke test manual en FacturaIA Sandbox vía agent-browser antes de mergear (así
> se verificó #685 — usuario `e2e+smoke@agentesia.madrid`, credenciales en
> `.env.test` del repo). Antes de tocar el Bloque 3 (conciliación), para el trabajo
> y pregunta a Manu la decisión de diseño abierta (logAgentAction explícito vs.
> ampliar `feed.ts` para leer `module_events`) — está descrita en la última
> sección del doc.
