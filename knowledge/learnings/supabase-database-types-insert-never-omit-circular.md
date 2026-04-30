---
title: supabase database.types — insert/update con omit genera never por referencia circular
date: 2026-04-30
source: claude-code-session
tags: [supabase, typescript, database-types, agency-portal]
---

Cuando añades una tabla manualmente a `database.types.ts` y defines Insert/Update como
`Omit<Row, 'id' | 'created_at'>`, TypeScript puede resolver la referencia circular a `never`,
haciendo que `from('tabla').insert(...)` falle en compilación.

**Fix**: escribir los campos explícitamente en Insert/Update, no usar Omit:

```ts
onboarding_messages: {
  Row: { id: string; session_id: string; role: 'user' | 'assistant'; content: string; created_at: string }
  Insert: { session_id: string; role: 'user' | 'assistant'; content: string }
  Update: { session_id?: string; role?: 'user' | 'assistant'; content?: string }
}
```

Además, Supabase 2.99 con `PostgrestVersion: "12"` no infiere el tipo desde el Database type
en `.select()` — sigue necesitando cast explícito: `as { data: Array<...> | null }`.
Los `.insert()` también pueden requerir `as never` si el tipo sigue sin resolverse.
