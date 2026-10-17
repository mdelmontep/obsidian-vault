---
title: ADR-032 — AS OAuth del MCP partido app↔servicio + hand-roll (no @jmondi)
date: 2026-06-18
status: accepted
tags: [adr, facturaia, mcp, oauth, seguridad]
---


> [!info] Portado al repo como **ADR-061** (30-ago-2026)
> El código de `facturaia` cita esta decisión desde `services/mcp-server/`, así
> que vive también en `facturaia/docs/decisions/ADR-061-el-as-oauth-del-mcp-esta-partido-app-servicio-y-va-hand-roll.md`,
> donde los tests pueden anclarla. Cambia el número porque el `ADR-032` del repo
> es otra decisión (el albarán valorado) y las dos series se citan igual; ver
> `facturaia/docs/decisions/NUMERACION.md`. **La copia del repo manda**: si algo
> cambia, se cambia allí y este documento se queda como está, con su fecha.

## Contexto
El servidor MCP remoto necesita OAuth 2.1 (issue 045). El servicio vive en `mcp.tufacturaia.com` y la sesión Supabase (cookies) en `app.tufacturaia.com`. El access token está fijado por el contrato 041 (user-token JWT ES256, ya verificado por la v1 en slice 044). El PRD había anotado usar `@jmondi/oauth2-server`.

## Opciones consideradas
Sesión en `/authorize`:
- **A** — `/authorize`+consent como rutas Next en el app (reusa la sesión presente); `/token`+JWKS en el servicio. No toca cookies.
- **B** — cookies en dominio padre `.tufacturaia.com` → toca config de cookies del app en prod (riesgo de regresión).
- **C** — redirect a login + ticket de un solo uso → más piezas y superficie a auditar.

Librería:
- **@jmondi** — AS de un solo proceso; con el split habría que configurarla en 2 mitades que solo comparten la BD, y sobreescribir su emisión de tokens para cumplir 041 → más código propio, no menos.
- **hand-roll** — sobre tablas 043 + validadores 045a (puros, test negativo) + contrato 041.

## Decisión
**A + hand-roll.** El split reusa el login probado del app sin tocar cookies de prod; con el token fijado por 041, hand-roll minimiza y aísla la lógica crítica (PKCE/redirect/scope/state ya en `oauth/policy.ts`), más auditable de cara al gate 047.

## Consecuencias
AS partido en 2 procesos que comparten las tablas 043 (BD = estado compartido). La clave privada ES256 de firma vive SOLO en el servicio (`/token`). Cerramos `@jmondi` y el dominio-padre de cookies. Todo el core OAuth (045-046) pasa por auditoría de seguridad humana (047) antes de prod.
