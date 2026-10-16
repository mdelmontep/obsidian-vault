---
title: al llamar a un endpoint nuevo de una api externa, revisa los scopes de la key de prod
date: 2026-10-16
source: agency-portal (#822, sync de TuFacturaIA)
tags: [api, integraciones, facturaia, backfill]
---
**Qué pasó:** el portal empezó a leer `GET /clientes/{id}` de TuFacturaIA. Los tests y el gate salieron en verde, pero la key de prod (`agency-portal-prod`) solo tenía scopes de facturas y presupuestos, así que cada lectura en prod daba 403. Además, el código convierte un fallo de lectura en «contacto no resuelto», así que la sincronización respondió 200 sin rellenar nada.

**Por qué no se vio:** los dobles de los tests no tienen scopes, y una key creada hace meses lleva los scopes de entonces. En TuFacturaIA no se pueden editar los scopes de una key existente; solo se crea una nueva o se revoca.

**Patrón:**
- Antes de desplegar código que llama a un endpoint nuevo, mira qué scope exige (`requireScope` en la ruta) y compáralo con los `scopes` de la key de prod (`api_keys` por `key_prefix`, los 16 primeros caracteres).
- Si el código degrada un fallo a «no resuelto», cuéntalo aparte en la respuesta (aquí `contactUnresolved`). Fue ese contador el que destapó los 23 de 23.
- Arreglo aplicado aquí: `array_append(scopes,'clientes:read')` con guardas de id, nombre, `revoked_at is null` y que no lo tuviera ya.
