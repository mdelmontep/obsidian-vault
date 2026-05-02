---
title: encryption key de credenciales en bd no es rotable in-place
date: 2026-05-02
source: claude-code-session
tags: [seguridad, criptografia, supabase, secrets]
---

Si cifras secrets en BD con AES-256-GCM usando una env var (`WEBHOOK_SIGNING_KEY`, `CREDENTIAL_ENCRYPTION_KEY`, etc.), esa key no se puede rotar sin perder el acceso a los secrets ya cifrados.

Cambiarla = todos los secrets en BD quedan ilegibles. Síntoma típico: `decryptSecret()` lanza "Unsupported state or unable to authenticate data" o, si la nueva key viene vacía, "KEY (>=32 chars) requerido" — y el dispatcher marca todas las entregas como `permanent_failure`.

Soluciones:
- Generar la key UNA vez y documentarla como inmutable.
- Si hay que rotar: regenerar todos los secrets cliente-lado (revocar webhooks/api-keys + crear nuevos), no rotar la key maestra.
- Para sistemas que sí necesiten rotación: añadir `key_id` por fila + tabla de keys vivas con migración progresiva.

Asumir por defecto: la primera key es para siempre. Apuntarla en password manager con nota explícita.
