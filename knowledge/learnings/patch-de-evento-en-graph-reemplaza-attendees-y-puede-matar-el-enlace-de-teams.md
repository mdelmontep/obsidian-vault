---
title: un patch parcial de evento en microsoft graph reemplaza attendees y puede matar el enlace de teams
date: 2026-07-29
source: claude-code-session
tags: [m365, microsoft-graph, calendario, api-externa, anti-patron]
---
`PATCH /me/events/{id}` parece seguro («solo mandas lo que cambias») pero tiene dos trampas documentadas en la propia doc de Microsoft, y las dos rompen hacia fuera:

1. **`body` + reunión online**: hay que **traer el `body` primero y preservar el meeting blob**; quitarlo **desactiva la reunión online**. O sea: escribir una nota en el cuerpo de un evento de Teams a ciegas **inutiliza el enlace de unión**. Peor que perder un campo.
2. **`attendees` es una colección que se REEMPLAZA**: un PATCH con `[Marta]` deja la reunión con Marta sola **y manda el aviso de actualización a todos los que acabas de borrar** — el fallo sale del sistema hacia terceros.

Regla: `updateEvent` **nunca** es un PATCH directo → **GET → fusionar en memoria → PATCH del objeto fusionado**, con test que fije que el `body` previo sobrevive. Es la versión cara del anti-patrón general de [[put-objeto-completo-borra-campos-no-mapeados]]: aquí no pierdes un dato, inutilizas la reunión.

Corolario de diseño para «edita el evento X»: no montar una tabla espejo con el `graphEventId` de lo que creó el agente — solo conocería sus propios eventos, y «la reunión del martes con X» suele haberla creado el usuario en Outlook o el cliente por invitación. Resolver **leyendo el calendario** cubre todos y no duplica estado que M365 ya posee.

Caso real: agh-iberica #580 (triaje). Ojo: `calendarView` no devuelve el `id` si no lo pides en `$select`, y un `createEvent` que devuelve `void` tira el id del evento recién creado.
