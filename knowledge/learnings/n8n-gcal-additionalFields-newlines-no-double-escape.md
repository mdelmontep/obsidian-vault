---
title: n8n GCal create description requiere `\n` no `\\n` para saltos de línea
date: 2026-05-25
source: claude-code-session
tags: [n8n, google-calendar, escaping]
---

En `Google Calendar > Create event > Additional Fields > Description`, el valor almacenado debe contener saltos de línea literales (`\n`, single backslash). Si guardas `\\n` en el JSON del workflow (por copy-paste de literal escapado), GCal lo recibe como texto `\n` literal y el evento aparece "todo de golpe" sin saltos.

Síntoma típico: description con `\nTel:\nCoche:` visible como una línea sólida en Calendar UI.

Fix vía API:
```python
# wrong: '=Cliente: {{ $json.name }}\\nTel:...' → GCal description con "\n" literal
# right: '=Cliente: {{ $json.name }}\nTel:...' → saltos reales
description = description.replace('\\n', '\n')
```

Caso real: EcoBox `Reservar_cita > GCal create` 2026-05-25. El blueprint del skill `agentesia-pollo-costco` venía con `\\n` legacy de un PUT antiguo.
