---
title: el dato canónico vive en el lote y el producto solo siembra
date: 2026-07-31
source: claude-code-session
tags: [inventario, erp, modelado, producto]
---
Antes de inventar un modelo de caducidad, miré Odoo (código de `product_expiry`, no solo la
doc), SAP ERP/S4 y Dynamics 365 BC. **Los tres coinciden**, así que la pregunta al cliente
ya tenía respuesta del sector:

- **El dato canónico vive SIEMPRE en el lote/partida.** La "vida útil" del producto es una
  SEMILLA de cálculo, nunca la verdad. Se materializa al recibir y desde ahí manda el lote.
- **Un flag explícito** (`use_expiration_date` en Odoo, `Use Expiration Dates` en BC) separa
  *"no caduca"* de *"caduca y no lo hemos apuntado"*. Sin él, un NULL significa las dos
  cosas, que es justo la pregunta que haría un inspector. **Ninguno usa `0` como centinela.**
- **Una vez la fecha está puesta, no se recalcula jamás.** Es el guard `and not
  lot.expiration_date` de Odoo. SAP hace lo contrario (una entrada posterior pisa la fecha
  manual) y su propia doc lo trata como comportamiento sorprendente: si la tecleó alguien
  mirando la etiqueta de la caja, ningún proceso la pisa.
- FEFO ordena `fecha ASC NULLS LAST`: un lote sin fecha se sirve el último, no se bloquea.

Lo que NO copié, y por qué: las cuatro fechas de Odoo (caducidad, consumo preferente,
retirada, alerta) no significan nada con vida útil de 48 h; y hacerla obligatoria produce
fechas inventadas, peor que un NULL honesto (Katana, Zoho y Holded la dejan opcional).

Y el matiz legal que invierte la intuición: lo que exige el Reglamento UE 931/2011 es el
**lote** y su rastro documental, no la caducidad. Un diseño con caducidad obligatoria y lote
opcional está al revés de la norma.
