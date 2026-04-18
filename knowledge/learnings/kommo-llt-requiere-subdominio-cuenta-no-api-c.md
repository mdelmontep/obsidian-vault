---
title: kommo long lived token requiere subdominio de cuenta, no api-c.kommo.com
date: 2026-04-18
source: claude-code-session
tags: [kommo, api, autenticacion]
---

Las llamadas API con Long Lived Token deben ir a `https://<cuenta>.kommo.com/api/v4/...`, NO a `api-c.kommo.com`.

Usar el dominio genérico `api-c.kommo.com` devuelve 401 "Account not found" aunque el token sea válido. Este es el dominio que usa OAuth2, pero LLT necesita el subdominio específico de la cuenta.

Ejemplo: para Clinica Zen → `https://citasclinicazenes.kommo.com/api/v4/leads`

Ver también: [[kommo-task-types-solo-se-crean-desde-ui]]
