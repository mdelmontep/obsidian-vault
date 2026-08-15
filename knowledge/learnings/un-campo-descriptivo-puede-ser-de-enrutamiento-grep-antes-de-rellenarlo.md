---
title: un campo que parece descriptivo puede ser de enrutamiento — grep dónde se consume antes de rellenarlo
date: 2026-08-15
source: claude-code-session
tags: [n8n, elphis, anti-patron, shape-compartido]
---

**Caso real (Centro Elphis, 2026-08-15):** al añadir el handoff de "paciente esperando en la consulta" puse `urgencia: 'alta'` — parecía metadato descriptivo para que recepción viera la prioridad. Pero tres workflows más abajo, `registrar-lead/Decidir etapa` hace `if (tipo === 'ingreso' || urgencia === 'alta') destino = 'ingreso'`: ese campo **elige a quién se avisa**. El aviso de un paciente plantado en la consulta habría salido al teléfono de ingresos residenciales en vez de a recepción, con el email etiquetado "⚡ INGRESO URGENTE".

**El patrón:** en un pipeline con varios saltos, un enum que en el productor lees como adjetivo (`urgencia`, `tipo`, `prioridad`, `categoria`) puede ser el discriminante de un `switch` en el consumidor. La pista de que es de control es que sus valores sean cerrados.

**Regla:** antes de rellenar un campo de un shape que cruza workflows/servicios, grep su nombre en TODOS los consumidores y mira si aparece en algún condicional. Si es de control, la información descriptiva va por otro campo libre (aquí, el texto de `motivo`, que ya viaja al WhatsApp y al email).

Corolario: lo cacé releyendo el consumidor **después** de aplicar el cambio, no antes. El coste de ese grep son 20 segundos.

Relacionado: [[el-else-de-un-clasificador-que-rellena-un-llm-debe-avisar-no-callar]] · [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]]
