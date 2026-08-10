---
title: resolver el destinatario por su clave, no por recencia ni por sufijo
date: 2026-08-10
source: claude-code-session
tags: [datos, whatsapp, scripts, verificacion, agh-iberica]
---
Un script de prueba elegía a quién mandar un WhatsApp con `order by created_at desc limit 1` sobre las 10 identidades del tenant. La más reciente **no** era el destinatario esperado: tres mensajes con los hilos de negocio de un usuario acabaron en el móvil de otra persona. La tabla tenía una columna `user_id` desde el principio.

Tres cosas que fallaron, y las dos últimas son las que se repiten:

- Al preguntar *«¿esto solo me llega a mí?»* se midió **el camino de producción** (que resolvía bien) en vez del camino **del script**. Una medición rigurosa del objeto equivocado convence más que no medir.
- «Fijar» el valor no lo verifica: pasar de «el más reciente» a «el que acaba en 034» **verifica exactamente lo mismo (nada)** y solo congela el error con aspecto de rigor.

**Patrón:** resolver por la clave que identifica (`user_id`), y además **aseverar el dueño y comparar** antes de enviar — `select user_id where external_id = <el resuelto>`, abortar si no coincide. La verificación buena no es «elegí bien», es *«el sistema me dice de quién es y lo comparo»*.

Corolario: un script que hace `curl` directo a la API **no hereda ninguna salvaguarda de la app** — ni la resolución de destinatario ni el registro. La tabla de entregas quedó vacía: sin rastro salvo en el proveedor.

Ver [[una-afirmacion-repetida-no-es-una-verificacion]].
