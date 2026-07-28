---
title: recordatorio a N horas sin ventana horaria escribe al cliente de madrugada
date: 2026-07-28
source: claude-code-session
tags: [recordatorios, whatsapp, ux, clinica-zen]
---
Un recordatorio definido como "X horas antes de la cita" y un scanner que corre 24/7
mandan mensajes a cualquier hora: con X=4 y un negocio que abre a las 10:00, TODA cita de
primera hora dispara un WhatsApp entre las 06:00 y las 07:00. Nadie lo diseñó así; sale
de componer dos decisiones razonables por separado.

Caso real (Clínica Zen): 28-jul 06:30, recordatorio de 4h de una cita de 10:30. Meses
funcionando sin que nadie lo mirara — el workflow estaba "en verde".

El offset relativo necesita SIEMPRE una ventana de emisión: si `hora_envío` cae fuera de
(09:00–21:30), adelantar al primer momento válido o suprimir ese aviso y dejar el de 24h.
Regla de revisión: para cada recordatorio relativo, restar el offset a la hora de APERTURA
del negocio — si da una hora que no mandarías tú a mano, está roto. Ver [[clinica-zen]]
