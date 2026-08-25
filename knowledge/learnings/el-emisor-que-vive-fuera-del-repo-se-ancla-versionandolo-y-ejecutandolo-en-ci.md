---
title: el emisor que vive fuera del repo se ancla versionándolo y ejecutando su código en CI
date: 2026-08-25
source: agency-portal
tags: [n8n, fixtures, contratos, testing]
---
Cuando quien te manda los eventos es un workflow de n8n del cliente, el fixture
escrito a mano miente y no hay forma de enterarse. La cura: **exportar el
workflow al repo** (`channels/kommo_n8n/n8n-emisor.json`) y que un test ejecute
su nodo Code de verdad contra el adaptador real:

```js
const run = new Function('$input', '$workflow', '$env', jsCode);
run({ all: () => items, first: () => items[0] }, { id }, env);
```

El fixture pasa a ser **la salida del emisor**, no una invención. En cuanto se
hizo, dos cosas que el fixture a mano daba por buenas resultaron falsas: el
webhook de mensajes de Kommo **no trae el teléfono** (había un camino "cubierto"
que en producción no existe) y `author.name` es PII que el emisor no debe
reenviar.

Al capturar payloads reales, cuidado con dos trampas: **anonimizar también las
URLs** (grabación, logs, pcap → `example.invalid`; el texto scrubbeado no sirve
si el enlace baja el audio real), y **no mandar los mensajes en bucle** — un
Chatwoot sella `created_at` con su reloj y no acepta backdating, así que los seis
salen en el mismo segundo y el fixture no prueba ni orden ni duración.
