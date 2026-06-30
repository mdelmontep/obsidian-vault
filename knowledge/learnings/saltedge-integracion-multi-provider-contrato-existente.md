---
title: integración nueva a una familia ya cubierta por un contrato compartido — buscar ESE contrato, no la plataforma de integraciones genérica
date: 2026-07-01
source: claude-code-session
tags: [arquitectura, integraciones, facturaia]
---

Al diseñar Salt Edge (provider PSD2/Open Banking nuevo) asumí inicialmente el patrón de
"plataforma de integraciones" genérica del repo (`src/lib/integrations/providers/*`,
`Provider` interface OAuth2/api_key/webhook). Existía un contrato MÁS específico y ya
maduro: `Psd2Provider` (`src/lib/conciliacion/psd2/types.ts`), con Tink/TrueLayer ya
implementados, tabla propia, cifrado propio, cron propio.

Síntoma genérico: un repo grande puede tener varios "sistemas de plugins" paralelos para
dominios distintos (integraciones genéricas vs. PSD2 vs. webhooks salientes vs. providers
de email...). El primero que encuentras explorando no es necesariamente el correcto para
tu dominio.

Fix: antes de planificar, grep por el nombre del dominio (`psd2`, `bank`, etc.) en TODO el
repo, no solo en la carpeta "integraciones" obvia. Un Explore agent dedicado a "¿existe ya
un contrato para esto?" antes de diseñar evita rehacer el plan a mitad de sesión.
