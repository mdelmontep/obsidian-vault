---
title: n8n emailSend con destinatario opcional → onError continueRegularOutput
date: 2026-05-25
source: claude-code-session
tags: [n8n, email, optional-fields]
---

Si `toEmail` puede venir vacío (campo opcional del cliente), por defecto `emailSend` lanza "No recipients defined" y rompe el workflow entero.

Fix: en el nodo emailSend setear `onError: continueRegularOutput`. Skip silencioso si no hay destinatario, downstream continúa.

```python
# por API
for n in wf['nodes']:
    if n['name'] == 'Email al cliente':
        n['onError'] = 'continueRegularOutput'
```

Útil cuando recoges email opcional en chatbot pero por voz no lo pides — el mismo workflow sirve ambos canales sin bifurcar.

Alternativa más estricta: IF node antes que solo deja pasar si `email` existe Y matches `/^[^@]+@[^@]+\.[^@]+$/`. Más verboso pero más explícito en el log de executions.

Caso real: EcoBox `Reservar_cita > Email al cliente` 2026-05-25 — voz no pide email, workflow no debe romper.
