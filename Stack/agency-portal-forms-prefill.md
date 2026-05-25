---
title: agency-portal — prefill de formularios desde queries del servidor
date: 2026-05-25
source: PR #73 (fix/invoice-prefill-client-fiscal)
tags: [agency-portal, forms, gotcha, nextjs]
---

# Prefill de formularios server→client

Patrón de bug recurrente en `(portal)/agency/*/new/page.tsx`: la página carga el detalle completo de una entidad (cliente, prospect, etc.) con todos sus campos, pero al pasar al form como `defaultX` sólo manda un subset (name/email), y el form sólo precarga ese subset. Resultado: campos derivados (fiscal, dirección, teléfono, etc.) salen vacíos aunque la entidad los tenga guardados.

## Caso PR #73 (factura nueva)

- `getAgencyClientDetail(clientId)` selecciona los 6 campos fiscales (`fiscal_name, nif_cif, fiscal_address, fiscal_city, fiscal_postal_code, fiscal_country`).
- `page.tsx` construía `defaultRecipient = { name, email, clientId }` — descartando todo el resto.
- Form inicializaba `recipientFiscal` solo desde `sourceQuote?.recipientFiscal`. Si no había sourceQuote → vacío.
- `handleRecipientChange` en el combobox ni siquiera copiaba `recipient.fiscal` aunque `RecipientOption.fiscal` venía cargado desde `listRecipientOptions`.

**Fix**: ensanchar el shape del `defaultRecipient` para incluir `FiscalData` + `phone`, inicializar todos los estados del form a partir de ahí, y en handlers de selección copiar el bloque completo (no campo a campo). Abrir el collapsible cuando hay datos prerellenados para que se vean.

## Regla — Why & How to apply

**Si una query del server-side ya carga campos opcionales/fiscales de una entidad, el form que la consume debe prerellenar TODOS esos campos, no solo los obvios.** El usuario edita la ficha del cliente esperando que esos datos se reutilicen en factura/quote/contract.

**Why**: el ROI de guardar datos en la ficha del cliente es justamente no reescribirlos en cada documento. Prerellenar a medias hace que el user no se fíe del sistema y reescriba todo manualmente — o peor, emita facturas con datos fiscales vacíos sin darse cuenta.

**How to apply**: al añadir un nuevo flujo `/agency/<entidad>/new` con `defaultX`/`sourceX`:
1. Listar todos los campos del form.
2. Listar todos los campos que la query ya devuelve para la fuente.
3. Mapear 1:1. Si un campo del form existe en la fuente, pasarlo.
4. Si el bloque fiscal/dirección está dentro de un collapsible, abrirlo cuando hay datos.
5. En handlers de combobox/select que cambian la fuente: copiar el bloque completo, no solo identidad.

## Patrón inverso a evitar

- Cargar el detalle completo en `page.tsx` y luego descartarlo en el spread al form.
- Confiar en que `sourceQuote` siempre existe (no es el caso en entrada manual ni en `?clientId=`).
- "Es opcional, que el user lo rellene" — esos campos ya están guardados, rellenarlos.

## Sitios donde aplicar la misma revisión

- `/agency/quotes/new` — ¿inicializa fiscal del cliente cuando viene de combobox de prospect/cliente?
- `/agency/contracts/new` — idem.
- `/agency/agency-invoices/*` — ya cubierto en este PR.

(Revisar caso por caso si el user lo reporta; no tocar preventivamente sin evidencia de bug.)

## Relacionado

- [[agentesia]] — hub
- PR #73: `fix/invoice-prefill-client-fiscal`
