---
title: PUT de objeto completo a una API externa borra campos que tu integración no mapea
date: 2026-07-08
source: claude-code-session
tags: [integraciones, api, seguridad-datos, holded]
---

Al escribir a una API externa (`PUT /recurso/:id`) con solo el subconjunto de campos que tu sistema conoce, si esa API hace reemplazo completo del objeto (no merge parcial), cualquier campo que la API tenía y tú no mapeas se pierde — se pisa a `null`/vacío.

Caso real: Holded devuelve `iban`, `swift`, `trade_name`, `client_record` en sus contactos; nuestro mapper solo conocía `name/code/vat_number/email/phone/bill_address`. Un `PUT` con ese subconjunto borró esos campos en 409 contactos reales.

**Antes de escribir a cualquier API externa con datos que no controlas por completo:**
1. Comprobar si el método de escritura es merge parcial (`PATCH` semántico) o reemplazo completo (`PUT` real) — no asumir por el nombre del verbo HTTP, verificarlo con un GET-antes-y-después real.
2. Si es reemplazo completo: hacer `GET` del objeto actual, fusionar solo tus campos conocidos sobre el resto, y mandar el objeto fusionado — nunca el subconjunto a ciegas.
3. Probar el primer write real contra una cuenta de prueba vacía, nunca una cuenta con datos de negocio reales — ver [[sync-bidireccional-anti-eco-hash-canonico]].
