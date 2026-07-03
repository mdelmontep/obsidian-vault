---
title: token de un solo uso respaldado por tabla propia — el envoltorio HMAC es redundante
date: 2026-07-03
source: claude-code-session
tags: [security, api-design, tokens]
---
Si un enlace/token de un solo uso se valida SIEMPRE contra una fila en BD (ledger con `used_at`/`expires_at` propios, nunca se confía en un payload re-decodificado del propio token), envolverlo en un JWT-ish firmado con HMAC (`base64url(payload).firma`) no aporta seguridad real — la firma solo protegería datos que la fila ya valida por su cuenta (p. ej. `exp`).

Ese envoltorio SÍ hace falta cuando el servidor confía en el contenido del token sin ir a BD (ej. JWTs stateless). Si hay ida a BD en cada consumo, basta con que el identificador (`jti`) sea aleatorio y suficientemente largo (80-96 bits de un solo golpe de `randomBytes`, sin cifrar) — infactible de adivinar en la ventana de TTL, sobre todo con rate-limit.

Caso real (facturaia, WS5 export por WhatsApp): token original ~150 caracteres (`base64url({jti,exp}).hmac`), feísimo para pegar en un mensaje. Quitar el envoltorio y usar el `jti` de 10 bytes tal cual como código de la URL (`/l/<jti>`) lo dejó en ~55 caracteres, sin perder seguridad — el `UPDATE ... WHERE jti=$1 AND used_at IS NULL AND expires_at>=now()` sigue siendo la única fuente de autorización real.
