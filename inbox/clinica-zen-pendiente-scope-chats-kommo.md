---
title: clinica zen - pendiente scope chats kommo
date: 2026-04-17
source: claude-code-session
tags: [clinica-zen, kommo, pendiente]
---
e ab
## Qué falta

Soporte Kommo debe habilitar el scope "Chats" en la cuenta `citasclinicazenes.kommo.com` (Account ID: 36308863, Integration Client ID: `751c9caa-58b3-4d0b-aa90-e4204739b94d`).

## Por qué

Sin el scope "Chats", el amojo_token (necesario para enviar mensajes por WhatsApp vía amojo API v1) hay que actualizarlo manualmente cada ~24h desde el navegador. Con el scope, se aplica el patrón Laserys y el token se renueva automáticamente en cada ejecución.

## Contacto

- Email: `support@kommo.com`
- Asunto y cuerpo ya redactados (en inglés) — buscar en la sesión de Claude Code del 2026-04-17

## Una vez resuelto

1. Crear nueva credencial OAuth2 en n8n con el scope "Chats"
2. Añadir nodo `get token` (patrón Laserys) antes de cada bloque de envío
3. Cambiar los 12 nodos HTTP Request para usar token dinámico en vez de Header Auth
4. Añadir typing entre mensajes (`POST amojo.kommo.com/v2/typing`)
5. Eliminar credencial Header Auth manual
6. Eliminar workflow test `xdSn2v2ac7IlGl65` si sigue activo
