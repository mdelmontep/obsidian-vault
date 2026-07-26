---
title: un fk restrict no sirve como regla de negocio porque no distingue estados
date: 2026-07-26
source: claude-code-session
tags: [postgres, schema, reglas-de-negocio, supabase]
---

Tentación: la FK ya tiene `ON DELETE RESTRICT`, así que copio ese bloqueo tal cual
a la regla de negocio ("no se puede borrar si tiene hijos"). El problema es que la
FK solo sabe si EXISTE una fila hija, no en qué ESTADO está el padre de esa fila.
Y casi siempre la regla real depende del estado.

Caso real (FacturaIA, mig 567 → 568): borrar una factura recibida duplicada se
bloqueaba si estaba en cualquier `fiscal_declaracion_snapshot`, copiando el
RESTRICT. Pero un snapshot de una declaración en `borrador` es un documento de
trabajo que se recalcula solo; lo intocable es una declaración ya revisada o
presentada. Con el bloqueo indiscriminado, y un cron que genera borradores cada
noche, **la función nació inservible**: cualquier duplicado dejaba de poder
borrarse en menos de un día, y recalcular la declaración lo volvía a meter en el
snapshot. Bloqueo circular.

Regla: la FK es la última red (integridad referencial), no la política. La política
va en la operación, distingue estados, y **arrastra** lo que solo existe por causa
del padre (ahí: la fila de snapshot de un borrador, y la conciliación bancaria de
una factura que no debería existir).

Corolario de método: lo destapó el guard de verificación del propio script de
limpieza, que abortó la transacción sin tocar nada. Un script de datos con guards
que comparan contra la medición no es burocracia — es lo que evita ejecutar sobre
un mundo que cambió desde que mediste.
