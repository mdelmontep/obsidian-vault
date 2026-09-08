---
title: reenganche que dispara por "último mensaje fue del bot + pasó tiempo" reabre conversaciones ya cerradas bien
date: 2026-08-04
source: clinica-zen
tags: [n8n, kommo, whatsapp, reenganche, clinica-zen]
---

Un workflow de "reenganche de conversaciones abandonadas" que dispara con la condición
`último_mensaje.tipo = 'ai' AND tiempo_transcurrido > X` es un falso positivo estructural: **toda**
conversación bien terminada también acaba con el bot teniendo la última palabra (la despedida) y
luego silencio. Esa condición no distingue "el paciente se fue a medio flujo" de "el paciente dijo
gracias y se despidió" — las dos formas de "el bot habló último y nadie contestó" son indistinguibles
sin mirar el CONTENIDO del último turno.

**Caso real**: Clínica Zen, paciente reservó cita, se despidió con "Gracias!", el bot respondió
"A ti. Que tengas buen día" — y 70 min después el workflow le mandó "¿Sigues por ahí?" igual.

**Fix intentado el 04-ago (insuficiente)**: mirar el último mensaje del HUMANO y excluir la sesión
si es un cierre corto reconocible (`gracias`, `vale gracias`, `adiós`... con regex anclado `^...$`).

**Medido el 08-sep: ese parche no podía funcionar, y el motivo es de diseño.** El prompt del agente
ordena variar la despedida (`AI Agent`, regla 14: «NUNCA uses la misma frase de cierre dos veces»),
así que la copy de cierre es un conjunto ABIERTO: cualquier lista de palabras clave se queda corta
por construcción. Y el turno humano tampoco discrimina — el bot cierra preguntando «¿necesitas algo
más?», así que una conversación bien terminada y un abandono real acaban idénticos.

**Fix real: decidir con ESTADO, no con texto.** Antes de reenganchar, leer el lead en el CRM y
descartar si tiene cita vigente, si está en un status cerrado o ya atendido, o si hay una palanca
manual de «no molestar». En Clínica Zen: campo `1864817` (fecha de la cita, la escriben tanto la rama
de chat como la de voz), `status_id`, `Apagar IA?` y `Derivación humana`.

**El status por sí solo NO basta**: tras la reserva por chat el lead sube a «Pendiente de asignar» y
ocho segundos después vuelve a «Contestados» — indistinguible de un abandono. En Clínica Zen lo hacen
dos nodos del MISMO workflow de chatbot, con el segundo `status_id` hardcodeado en el `jsonBody` de
una llamada HTTP. Y ése es el punto: **un status que cualquier nodo puede pisar no sirve como fuente
de verdad**; el campo de la cita sí.

**Método, que aquí costó dos diagnósticos falsos**: para explicar un evento pasado hay que leer el
`workflowData` incrustado en la ejecución, no el estado vivo del workflow. El vivo es de hoy; el
evento es de ayer. Leer el vivo me hizo afirmar dos veces que el culpable estaba fuera de n8n, cuando
el parámetro que lo causaba había sido retirado entre medias. Lo que discrimina es el CAMPO de la cita. Caso medido: lead 38845044, cita escrita a las
16:38:46 del 07-sep, reenganche enviado a las 18:00:59 con el lead en «Contestados».

**El descarte SÍ hay que persistirlo**, y esto costó dos intentos: inventarse un `status` reventó
contra un CHECK que nadie leyó, y esquivarlo dejando de escribir fila fue PEOR —el descarte
recirculaba cada pasada—. Ver
[[un-descarte-que-no-se-persiste-recircula-y-con-limit-desplaza-a-los-reales]].

**Transversal, revisado el 08-sep contra el vault.** El único otro cliente con reactivación
documentada es Simarro ([[llamadas-outbound-reactivacion]]), y **es inmune a este fallo**: selecciona
por ESTADO —etapa elegible, consentimiento, intentos <3, ≥10 días desde el CF «último intento»— sin
mirar quién habló el último. Es el diseño que este learning prescribe, escrito tres meses antes.

Lo que sí comparte es la otra mitad del problema, la que costó dos intentos aquí: **el freno depende
de que se escriba la marca**. Simarro incrementa `Intentos` y `Último intento` sólo si la llamada
llegó a lanzarse; si el lanzamiento falla, el lead se queda elegible y vuelve al día siguiente. Con
un cron diario y un cap de 3 eso no revienta nada, pero es la misma forma: *el descarte que no se
persiste recircula*. Sin verificar en el workflow (`2LqwDgLecHwjgIQl`, INACTIVO a fecha de hoy).

Las dos preguntas para cualquier reenganche nuevo, en este orden:
1. ¿Decide por estado o por texto? Si es por texto, está roto por construcción.
2. ¿Qué pasa en la pasada SIGUIENTE con lo que acaba de descartar? Si no queda marcado, recircula —
   y si la consulta lleva `LIMIT`, los descartes desplazan a los casos reales.
