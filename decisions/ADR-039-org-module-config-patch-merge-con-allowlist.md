---
title: ADR-039 — org_module_config.config se escribe con PATCH de merge por clave + allowlist del schema resuelto (no replace, no RPC atómica en v1)
date: 2026-07-25
status: accepted
tags: [adr, facturaia, jsonb, seguridad-datos]
---

## Contexto

`org_module_config.config` es un jsonb con **13 escritores** (endpoint de módulos, PUT admin, wizard
fiscal, saldo manual de cashflow, prompt de voz, checkout de billing, toggles de cliente). El
`PATCH /api/modules/[id]` hacía upsert del objeto entero, así que guardar la config de un módulo
borraba claves de otros subsistemas: el saldo bancario inicial manual y el borrador del wizard fiscal
se perdían en silencio. Además permitía escribir `prompt_override` del agente de voz saltándose el
endpoint que sí tiene If-Match, versionado y audit.

## Opciones consideradas

- **A — Merge por clave en servidor + allowlist del schema resuelto + `unset` explícito + 422 en
  claves reservadas.** Cualquier cliente parcial futuro es seguro por construcción. TOCTOU de ms
  entre el select y el upsert. Lógica en TS, testeable sin BD.
- **B — Replace del bloque-schema y preservar solo lo ajeno.** No arregla el caso real: un cliente que
  conoce 3 de las 9 claves del mismo schema seguiría borrando las otras 6, ahora desde el servidor.
- **C — RPC `SECURITY DEFINER` con `config = (config - drop) || patch`.** Único plenamente libre de
  TOCTOU. Exige migración, `REVOKE ... FROM PUBLIC, anon` y su test de seguridad; y deja el gate de
  tests sin poder aserverar el objeto mergeado (solo los argumentos del RPC).
- **D — Que cada cliente relea y reenvíe el jsonb completo.** Es lo que ya hacía y es el bug: el
  cliente reenvía un snapshot rancio.

## Decisión

**A**, porque el daño que motiva el ADR desaparece con el merge, no con el locking: en cuanto el
payload solo puede contener claves de la allowlist, el modal ya no tiene forma de expresar "borra el
saldo manual" por rancio que tenga el estado. `If-Match` se ofrece **opcional** (mismo contrato que el
endpoint de voz) para quien quiera detectar escrituras concurrentes. La allowlist sale del schema
**resuelto** (`module_metadata.config_schema` con fallback al catálogo), no del catálogo, porque la UI
renderiza el resuelto y si no coinciden hay campos que se guardan sin validar.

## Consecuencias

- El verbo pasa a significar lo que dice: PATCH parcial. Borrar exige `unset: string[]` explícito y
  limitado a la allowlist; el reset duro sigue siendo el `DELETE` de admin.
- Una clave del schema con valor obsoleto ya no "vuelve al default nuevo" por omisión. Aceptable:
  `getModuleConfig` mergea defaults por debajo.
- Las claves de sistema quedan declaradas en un solo sitio (`RESERVED_CONFIG_KEYS`) y con un
  invariante testeado: una reservada nunca puede estar en un schema, para que no se pueda reabrir el
  bypass desde `/admin/modules`.
- **C queda anotada** para cuando se observe una carrera real, no antes.
- Cierra como opción el upsert de jsonb parcial desde componentes cliente (test estructural que lo
  impide).

## Enmienda (2026-07-25) — la allowlist de ESCRITURA es la unión, no el override

Al endurecer el contrato apareció un efecto no previsto: el schema resuelto es `override ?? catálogo`,
así que una clave que el override de `module_metadata` **no declara** salía de la allowlist y quedaba
inescribible mientras el backend la seguía leyendo. Real en prod: el override de `fiscal` tiene 12
campos y no incluye los 8 `pgc_cuenta_*` del export de asientos → congelados en su default.

Decidido: separar **schema de render** (el override, que sí puede ocultar un campo) del **schema de
escritura** (`writeSchema` = override ∪ catálogo, ganando el override en el campo que declara). El
catálogo es el contrato del código; el override personaliza presentación y límites, no puede convertir
en inescribible algo que el código lee. Descartada la alternativa de arreglar solo el dato en prod: deja
el footgun abierto para el siguiente override que alguien recorte.

Refuerzos en el mismo sentido: el `PUT /api/admin/modules/[id]` rechaza con 422 un schema que declare
una clave reservada (antes solo lo impedía el invariante del catálogo, y el schema de BD no pasaba por
ahí), y deja de estripar `pattern`/`patternMessage`/`maxLength`/`preview`, con un test que compara el
Zod contra `ModuleConfigFieldDefault`.

Ver [[jsonb-compartido-varios-escritores-patch-parcial-borra-claves-ajenas]] ·
[[override-de-bd-que-sustituye-al-schema-del-codigo-congela-claves]] · [[facturaia]]
