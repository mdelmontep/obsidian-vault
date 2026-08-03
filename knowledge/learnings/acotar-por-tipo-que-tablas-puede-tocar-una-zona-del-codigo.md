---
title: acotar por TIPO qué tablas puede tocar una zona, no por convenio ni por revisión
date: 2026-08-03
source: claude-code-session
tags: [typescript, supabase, multi-tenant, arquitectura]
---

Un panel de administración usa `service_role` y **salta RLS por definición**: ahí
`db.from('leads').select('*')` devuelve los datos de todos los clientes, compila, pasa el
lint y pasa los tests. No hay nada que pueda cazarlo — es exactamente lo que ese cliente sabe
hacer. Un comentario no lo impide; una revisión tampoco, porque la línea es indistinguible de
una legítima.

Lo impide que el TIPO no sepa nombrar la tabla:

```ts
type TablasDeCenso = Pick<Database['public']['Tables'], 'organizations' | 'profiles' | …>
type DbDeCenso = { public: Omit<Database['public'], 'Tables'> & { Tables: TablasDeCenso } }
createClient<DbDeCenso, 'public'>(url, key)   // .from('leads') NO COMPILA
```

`Omit` + intersección en vez de escribir la forma a mano: enums, funciones y el resto del
esquema siguen siendo los generados, así que una migración llega sola.

Y el rojo se demuestra con un `.test-d.ts` de `@ts-expect-error`: al quitar el recorte, las
directivas quedan «sin usar» y **el typecheck falla**. El guard no es un test, es `tsc`.
