---
title: la cuota de la api de holded es por mes natural y su ui la desglosa por endpoint
date: 2026-10-04
source: centro-elphis (holded-migracion)
tags: [holded, api, cuota, observabilidad]
---

- La cuota (7.500 llamadas en el plan de Elphis) es **por cuenta y por mes natural**: se reinicia el día 1, no en ventana móvil.
- **Configuración › Desarrolladores › Uso de la API** desglosa por endpoint y por token. Holded etiqueta las llamadas a `/contacts` como `/api/v2/contact-groups`.
- Pasarse no rechaza de inmediato: en octubre-2026, 12.928/7.500 con **0 respuestas 429**; Holded solo avisa de que puede bloquear.
- Gotcha: un contador propio que solo suma en el workflow de producción se queda corto en cuanto un script (e2e, volcados) llama directo. En Elphis faltaban 7.310 llamadas. **Fix**: el cliente HTTP compartido de los scripts también suma al mismo contador (`crm_api_usage`), en lotes y con `atexit`.
- Si hay que subir el tope un solo mes, usar una clave por mes (`holded_quota_month_<YYYY-MM>`) con `COALESCE` a la general, para que vuelva sola el mes siguiente.
