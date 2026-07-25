---
title: un override de BD que SUSTITUYE al schema del código vuelve inescribibles las claves que omite
date: 2026-07-25
source: claude-code-session facturaia
tags: [arquitectura, config, jsonb, allowlist, admin]
---

Patrón habitual: el código declara un schema de configuración (catálogo) y una tabla permite a un
superadmin **sobreescribirlo** por entidad. El resolvedor casi siempre hace `override ?? catalogo`, es
decir **reemplaza el schema entero**. Inocuo mientras el schema solo pinta formularios.

Deja de serlo en cuanto ese schema pasa a ser la **allowlist de escritura** (endurecer el contrato es lo
que lo activa): una clave que el override no declara sale de la allowlist y queda **inescribible**,
mientras el backend la sigue leyendo. Efecto: el ajuste se congela en su default y no hay vía de cambio.
No es teórico — el override de `fiscal` en producción tenía 12 campos y no incluía los 8 `pgc_cuenta_*`
que lee el export de asientos contables.

- **Separa schema de RENDER de schema de ESCRITURA.** El de escritura es la UNIÓN (override ∪ catálogo,
  ganando el override en el campo que declara). Recortar el override puede ocultar un campo del
  formulario; no puede convertir en inescribible algo que el código lee.
- Ampliar solo la allowlist no basta: si la sanitización construye la salida iterando el schema, la clave
  pasa el filtro y se cae **en silencio**. La unión tiene que ser del schema, no del set de claves.
- El endpoint que guarda el override es un punto de entrada: valida ahí lo que no puede declararse
  (claves de sistema) y **no estripes props** — un `z.object()` sin `pattern`/`maxLength` las borra al
  guardar y con ellas su validación. Test que compare el Zod con la interfaz, o vuelve a pasar.

Relacionado: [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]] ·
[[ADR-039-org-module-config-patch-merge-con-allowlist]]
