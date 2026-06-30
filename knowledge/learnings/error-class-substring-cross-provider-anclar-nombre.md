---
title: detección de error por substring en módulo multi-provider — anclar al nombre del provider o falsos positivos cruzados
date: 2026-07-01
source: claude-code-session
tags: [error-handling, multi-provider, facturaia]
---

Un helper tipo `isAuthClassProviderError(msg)` que clasifica errores por substring
(`/\bTokenError\b/`, `/\bConnectionDisabled\b/`) y sirve a VARIOS providers de la misma
familia (PSD2: Tink/TrueLayer/Salt Edge) es peligroso si las señales no están ancladas al
provider que las define. Nombres de error class genéricos de un provider (Salt Edge:
`TokenError`) pueden aparecer por azar en el body crudo de un error 5xx de OTRO provider
(Tink/TrueLayer embeben el texto de su propia respuesta HTTP en el mensaje de Error) y
disparar una clasificación equivocada (ej. marcar un consent en `error` y notificar
"reconecta tu banco" por un blip de red, no por un fallo real).

Fix: ancla el regex a que el mensaje mencione el nombre del provider que originó esa señal
(`/Salt Edge[^]*\bTokenError\b/`), no solo al nombre de la clase. Detectado en code-review
adversarial (3 agentes independientes lo señalaron por separado) — no salta a la vista en
una revisión normal porque cada caso aislado (mensaje de Salt Edge real) parece correcto.
