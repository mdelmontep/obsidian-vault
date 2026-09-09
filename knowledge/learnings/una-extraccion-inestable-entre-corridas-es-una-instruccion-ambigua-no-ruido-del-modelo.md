---
title: una extracción inestable entre corridas es una instrucción ambigua, no ruido del modelo
date: 2026-09-09
source: centro-elphis
tags: [llm, extraccion, crm, retell, diagnostico]
---
El extractor de voz devolvía `dv_nombre` distinto en cada corrida del MISMO caso: `Sin nombre`,
`Carlos Sánchez`, `Marta Sánchez` en tres versiones seguidas. La tentación es tratarlo como
varianza del modelo y subir el determinismo. No lo era: la descripción decía *"nombre de la
persona que va a ser atendida"* y en una llamada de un familiar hay **dos** personas que encajan.
El modelo no dudaba, elegía — y cada vez una.

Regla: **cuando un campo extraído oscila entre valores que son todos defendibles, la instrucción
nombra mal a la entidad.** Si oscila entre un valor bueno y basura, entonces sí es el modelo.

El fondo era peor: el consumidor (`Upsert contacto` de Clientify) escribe ese campo como nombre
del contacto, y el contacto se identifica **por el teléfono de quien llama**. La descripción
apuntaba al paciente; la clave, al llamante. Fix: la descripción nombra al titular de la clave
del upsert ("quien está llamando, aunque llame por otra persona"). Medido: 3/3 aciertos en dos
corridas, frente a 0-1/3 antes.

Ver [[telefono-como-identity-key-en-upsert-crm-colisiona-si-se-comparte]] · [[un-campo-descriptivo-puede-ser-de-enrutamiento-grep-antes-de-rellenarlo]]
