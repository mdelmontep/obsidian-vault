---
title: un cursor incremental que avanza sobre lo que falló pierde el documento para siempre
date: 2026-09-05
source: facturaia
tags: [integraciones, sync, cursor, fail-closed, facturadirecta]
---
Un pull incremental (`minModificationDate` + cursor persistido) que guarda el **máximo** de todo lo VISTO deja por detrás del cursor lo que rechazó. Si el rechazo es fail-closed y determinista —una línea sin código de impuesto, un contacto borrado en el origen—, ese documento no vuelve a mirarse **nunca**: solo entraría si alguien lo modifica en el origen.

El solape de seguridad (`OVERLAP_MS`) parece cubrirlo y no cubre nada: solo alcanza a lo que falló al filo de la ventana. Caso real (FacturaDirecta, 4-sep-2026): dos gastos rechazados el mismo día con **16,5 min** de diferencia y solape de **10 min** → el nuevo se reintentaba cada cuarto de hora (13 fallos registrados) y el viejo, cero veces. La sync se declaraba al día con un documento perdido.

Fix: **anclar el cursor al fallo MÁS ANTIGUO de la pasada** (`min(minFallo, maxOk)`). Retroceder es gratis si re-escanear es idempotente (lo ya importado se salta por su fila del map). Dos detalles que no son opcionales: clasificar «ha fallado» por el **contador de errores antes/después**, no por lo que devuelva la tarea (suelen mutar un acumulador y no devolver nada); y **excepción por truncamiento** — si la pasada agota el tope de páginas sin llegar al final, anclar congela el cursor ahí para siempre, así que ahí sí se avanza: perder uno es mejor que no importar ninguno.

El síntoma que lo delata en producción: un contador de errores **estable** pasada tras pasada. Ver [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] · [[marcar-enviado-antes-de-enviar-pierde-el-mensaje-sin-reintento]]
