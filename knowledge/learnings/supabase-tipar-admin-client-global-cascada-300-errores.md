---
title: tipar createAdminClient con <Database> cascadea 300+ errores en codebase grande
date: 2026-07-02
source: claude-code-session
tags: [supabase, typescript, deuda-tecnica, facturaia]
---
En un codebase grande con muchas queries `admin.from().select()`/`.insert()` sin tipar,
pasar `createClient()` → `createClient<Database>()` NO es un cambio local: convierte
CADA query del app en type-checked contra el schema. En FacturaIA destapó 300+ errores
(jsonb `Json` no acepta objetos tipados en insert/upsert, indexar `Json` con string,
`Date(string|null)`) por todo el árbol, incluidos núcleos (create-document, verifactu,
notifications, sepa).

Patrón: generar `database.types.ts` es barato y seguro (artefacto + script `gen:types`),
pero **tipar el cliente global es una migración grande e independiente**, no una tarea de
"limpieza". Fix acotado: dejar el cliente sin tipar globalmente y usar cast local opt-in
`admin as SupabaseClient<Database>` por call-site donde quieras type-safety. Los `as any`
sobre el cliente untyped se pueden quitar sin coste (el cliente ya es `any`).
Ver [[defense-in-depth-estado-activo-cuando-admin-client-bypasa-rls]].
