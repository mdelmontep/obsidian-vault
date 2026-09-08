---
title: created_by 0 no atribuye una carga masiva; el control es crear la entidad tú
date: 2026-09-09
source: simarro
tags: [kommo, crm, forense, atribucion]
---
Ante "¿quién subió estos 1.850 contactos?", Kommo devuelve `created_by: 0` en la ficha **y** en el
evento `contact_added`. Tentador leerlo como la firma de una integración concreta. No lo es.

**El control**: creé un contacto por API con mi propio token y salió también `created_by: 0`, igual
que mis 18 importados. Así que el cero solo significa **"no fue un usuario pulsando en la UI"** —
no distingue qué integración, ni siquiera si fue un script a pelo.

Lo que sí atribuye es `responsible_user_id`: es el usuario que el script puso en el payload, así que
delata **la cuenta cuyo token se usó**. Ahí se vio que la carga salió de nuestro lado.

Patrón general, más allá de Kommo: **un campo de auditoría solo prueba lo que discrimina**. Antes de
concluir de un valor, reprodúcelo tú por la vía que sospechas y comprueba que sale distinto. Si sale
igual, ese campo no era evidencia. Barato: una entidad desechable.

Corolario Kommo: el registro de quién conectó cada integración no está en la API, solo en la UI.
