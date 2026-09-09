---
title: un sentinel de ausencia es una cadena no vacía — normalízalo en el origen
date: 2026-09-09
source: centro-elphis
tags: [llm, contratos, n8n, crm, anti-patron]
---
Un extractor LLM no puede devolver `null` de forma fiable, así que se le pide un **sentinel**:
"si no hay nombre o lo transcrito no lo parece, devuelve exactamente `Sin nombre`". Correcto en
esa capa. El problema está en la siguiente: aguas abajo el guard era

```js
name_is_placeholder = !(nombre || '').trim()   // "Sin nombre" es truthy → false
first_name = nombre.trim().split(' ')[0]       // → "Sin" / "nombre"
```

El sentinel viajaba como un nombre real y habría creado en el CRM un contacto llamado *Sin
nombre*, saltándose la rama de placeholder que existía justo para eso. No había pasado todavía
(0 en Clientify, verificado por API), pero el camino llevaba abierto dos versiones.

Regla: **el sentinel se traduce a ausencia en el PRIMER nodo que lo recibe**, no en cada
consumidor — aquí eran seis expresiones distintas leyendo el mismo campo, y basta olvidar una.
Y el regex debe anclarse (`/^sin\s+nombre$/i`), o te comes a un "Sinforosa Nombela".

Ver [[una-extraccion-inestable-entre-corridas-es-una-instruccion-ambigua-no-ruido-del-modelo]]
