---
title: un método sin llamantes puede tener el guard ausente y su comentario afirmar que está
date: 2026-08-07
source: claude-code-session
tags: [seguridad, multi-tenant, code-review, deuda]
---
Código implementado **y sin un solo llamante** no está probado por el uso: nada lo ejerce, así que un
guard que falta no se manifiesta. Cablearlo es lo que lo arma — y ese día el fallo parece del cambio
nuevo, no de la deuda que ya estaba.

Caso real (AGH #1030): `ReminderStore.cancel` filtraba por `WHERE tenant_id AND id`, **sin
`owner_user_id`** — o sea, un comercial podía cancelar el recordatorio de otro. Llevaba encima un
comentario que empezaba por *«GUARD: filtro por (tenant, id)»* y un docstring hermano que afirmaba
*«el guard de owner lo pone quien llama»*. **No lo ponía nadie**, porque no había llamantes.

- Antes de cablear un método muerto, **lee su guard, no su comentario**: el comentario describe la
  intención de quien lo escribió, no lo que quedó.
- `grep -rn "<método>"` y si solo salen la interfaz y sus implementaciones, trátalo como código
  **nuevo** en la revisión, no como código existente que ya funcionaba.
- El caso que lo caza es *«el de otro owner no se puede tocar»*, y contra **BD real**: un fake
  tenant-scoped lo esconde. Hermano de [[tests-contra-fakes-hornean-la-premisa]].
