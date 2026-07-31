---
title: el override numérico va en una vista LOCAL al módulo que escribe, no en el Database global
date: 2026-07-02
updated: 2026-07-31
source: claude-code-session
tags: [supabase, typescript, fiscal, type-safety]
---
`supabase gen types` tipa NUMERIC como `number`, pero PostgREST acepta strings (y
Postgres los parsea con precisión exacta). Si persistes céntimos `bigint`
serializados a string, el cliente tipado rechaza el insert.

**Corregido 31-jul: el fix NO es un override global.** El `database-overrides.ts`
que ensanchaba `fiscal_declaracion_snapshot` cambiaba la identidad estructural de
`Database`; TS dejaba de relacionarlo con el generado por la vía rápida y hacía la
comparación completa, así que añadir CUALQUIER tabla nueva reventaba el typecheck
con errores en ficheros del módulo fiscal ajenos al cambio. Trampa de diagnóstico,
no solo error de tipos: señala ficheros que quien hizo el cambio no ha tocado.

Medido antes de rediseñar: quitar el override dejaba **1 error, en el único sitio
del repo que escribe esos strings**; el escenario que antes daba 61 errores en 43
ficheros pasó a **0 colaterales**. Un ensanche global para un caso local.

Patrón correcto: vista tipada local en ese módulo, casteando el **cliente** y no
las filas (así conserva los tipos del query builder en vez de un stub a mano). Y un
test de identidad `Identical<Database, DatabaseGenerated>` que falla en el
TYPECHECK si alguien reabre el override — ver
[[un-comentario-que-afirma-una-invariante-es-una-deuda-de-test]].
NUNCA editar `database.types.ts` a mano. Caso real: FacturaIA `qa-027`, PR #1402.
