---
title: void sobre un builder de supabase-js = la query nunca se ejecuta
date: 2026-07-03
source: claude-code-session
tags: [supabase, postgrest, bugs-silenciosos, fire-and-forget]
---
Los builders de PostgREST (`.from().upsert/delete/update/select`) son thenables
LAZY: la request solo se envía al hacer `await` o `.then()`. Un
`void admin.from(x).delete().eq(...)` para "fire-and-forget" es un NO-OP
silencioso — compila, los tests con mocks pasan (el mock registra la llamada
al método), y en prod no pasa nada.
Caso real FacturaIA (bot WhatsApp "amnésico", 2026-07-03): el upsert de la
pregunta pendiente y 4 deletes de intents nunca ejecutaron; una fila "borrada"
dos veces seguía viva desde el 30-jun. PR #676.
Regla: fire-and-forget con builders = `void x.then(() => {})` o awaited;
NUNCA `void <builder>` a secas. (storage-js y fetch son Promises reales — ahí
`void` sí ejecuta.) Grep de auditoría: `void \w+\.from\(` sin `.then`.
