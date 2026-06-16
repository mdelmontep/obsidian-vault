---
title: un smoke que replica los inserts a mano no ejerce el motor real ni sus checks
date: 2026-06-16
source: claude-code-session
tags: [testing, smoke, e2e, supabase, postgres]
---
Un smoke que **recrea** la escritura con `INSERT` directo (eligiendo a mano
valores válidos) da falsa confianza: NO pasa por el motor de producción, que
puede elegir OTROS valores y violar un CHECK.

Caso TuFacturaIA (emitir-ticket): el endpoint pasaba `source:'web'` →
`createDocument` escribía `facturas.fuente='web'`, que viola `facturas_fuente_check`
(solo manual/whatsapp/email/telegram/camara/api/voice/mobile) → 500. El smoke de
BD insertaba la factura directo con `fuente='manual'` (válido a mano) → verde en
falso. **Solo lo cazó el E2E de navegador** (Playwright) que pega al endpoint real
→ `createDocument` → constraint.

Regla: smokea el **entry point real** (endpoint/UI), no una réplica de los INSERT.
El smoke en transacción-rollback ([[smoke-prod-en-transaccion-rollback]]) es ideal
para RPCs/triggers, pero si bypassa el motor que arma el payload, no ve sus bugs.
Relacionado: [[enum-nuevo-en-codigo-sin-ampliar-check-bd-rompe-insert-silencioso]].
