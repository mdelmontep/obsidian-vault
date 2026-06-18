---
title: revocación de grant oauth debe comprobarse en cada resource server que acepte el token, no solo en el gateway
date: 2026-06-18
source: claude-code-session
tags: [oauth, seguridad, jwt, mcp, facturaia]
---

Si un mismo JWT (access token) lo aceptan VARIAS superficies, comprobar la
revocación solo en una (el gateway) no protege: el token sigue valiendo contra
las otras hasta su `exp`.

Caso real (TuFacturaIA MCP, gate 059): `isGrantRevoked(gid)` se chequeaba en el
gateway MCP pero NO en `authenticateV1`. Como `/api/v1/*` es internet-facing y
acepta el mismo user-token, un access token de grant revocado seguía válido ~1h
saltándose el gateway. Un access token stateless NO se entera de la revocación
por sí mismo.

Fix: comprobar revocación en CADA resource server que verifique el token, y
**fail-closed** (error de consulta → tratar como revocado). El TTL corto del
access token NO sustituye al chequeo si el sistema promete revocación inmediata.

Ver [[revocacion-jwt-stateless-tabla-dedicada-no-inferir-de-filas-de-token]] ·
[[signOut-solo-invalida-refresh-no-access-token]] · [[remote-mcp-exige-oauth-no-api-key-estatica]]
